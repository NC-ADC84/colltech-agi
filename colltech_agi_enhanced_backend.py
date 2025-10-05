"""
CollTech-AGI Enhanced Backend
Adds LLM API integration, web search, and file system access
"""

import os
import json
import importlib.util
if importlib.util.find_spec("requests") is not None:
    import importlib
    requests = importlib.import_module("requests")
else:
    # Minimal fallback implementation of requests.get/post using urllib
    import urllib.request
    import urllib.parse
    import ssl

    class SimpleResponse:
        def __init__(self, status, content, headers):
            self.status_code = status
            self.content = content
            self.headers = headers

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP Error: {self.status_code}")

        def json(self):
            return json.loads(self.content.decode('utf-8'))

        @property
        def text(self):
            return self.content.decode('utf-8')

    def _perform_request(method, url, headers=None, data=None, timeout=None):
        headers = headers or {}
        data_bytes = None
        if data is not None:
            # If data is a dict or list, serialize as JSON
            if isinstance(data, (dict, list)):
                data_bytes = json.dumps(data).encode('utf-8')
                if 'Content-Type' not in headers:
                    headers['Content-Type'] = 'application/json'
            elif isinstance(data, str):
                data_bytes = data.encode('utf-8')
            elif isinstance(data, (bytes, bytearray)):
                data_bytes = data
            else:
                data_bytes = str(data).encode('utf-8')

        req = urllib.request.Request(url, data=data_bytes, headers=headers or {}, method=method.upper())
        context = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
            content = resp.read()
            return SimpleResponse(resp.getcode(), content, dict(resp.getheaders()))

    def _get(url, params=None, headers=None, timeout=None):
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        return _perform_request('GET', url, headers=headers, data=None, timeout=timeout)

    def _post(url, json=None, headers=None, timeout=None):
        return _perform_request('POST', url, headers=headers, data=json, timeout=timeout)

    class _RequestsModule:
        get = staticmethod(_get)
        post = staticmethod(_post)

    requests = _RequestsModule()

from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMIntegration:
    """Integration with LLM APIs (OpenAI, Anthropic, etc.)"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        self.provider = provider
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.base_url = self._get_base_url()
        
    def _get_base_url(self) -> str:
        """Get API base URL for provider"""
        urls = {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "local": "http://localhost:11434"  # Ollama default
        }
        return urls.get(self.provider, urls["openai"])
    
    def generate_response(self, prompt: str, personality: str = "lyra", 
                         mode: str = "conscious", **kwargs) -> Dict[str, Any]:
        """Generate response using LLM API"""
        
        if not self.api_key and self.provider != "local":
            return {
                "response": f"[{personality.upper()}] {self._get_simulated_response(prompt, personality)}",
                "metadata": {"source": "simulated", "reason": "no_api_key"}
            }
        
        try:
            if self.provider == "openai":
                return self._call_openai(prompt, personality, mode, **kwargs)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, personality, mode, **kwargs)
            elif self.provider == "local":
                return self._call_local_llm(prompt, personality, mode, **kwargs)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
                
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            return {
                "response": f"[{personality.upper()}] {self._get_simulated_response(prompt, personality)}",
                "metadata": {"source": "simulated", "reason": "api_error", "error": str(e)}
            }
    
    def _call_openai(self, prompt: str, personality: str, mode: str, **kwargs) -> Dict[str, Any]:
        """Call OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = self._build_system_prompt(personality, mode)
        
        data = {
            "model": kwargs.get("model", "gpt-4"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            "response": result["choices"][0]["message"]["content"],
            "metadata": {
                "source": "openai",
                "model": data["model"],
                "tokens": result.get("usage", {})
            }
        }
    
    def _call_anthropic(self, prompt: str, personality: str, mode: str, **kwargs) -> Dict[str, Any]:
        """Call Anthropic Claude API"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        system_prompt = self._build_system_prompt(personality, mode)
        
        data = {
            "model": kwargs.get("model", "claude-3-sonnet-20240229"),
            "max_tokens": kwargs.get("max_tokens", 1000),
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            "response": result["content"][0]["text"],
            "metadata": {
                "source": "anthropic",
                "model": data["model"],
                "tokens": result.get("usage", {})
            }
        }
    
    def _call_local_llm(self, prompt: str, personality: str, mode: str, **kwargs) -> Dict[str, Any]:
        """Call local LLM (Ollama)"""
        system_prompt = self._build_system_prompt(personality, mode)
        
        data = {
            "model": kwargs.get("model", "llama2"),
            "prompt": f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:",
            "stream": False
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=data,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        return {
            "response": result["response"],
            "metadata": {
                "source": "local_llm",
                "model": data["model"]
            }
        }
    
    def _build_system_prompt(self, personality: str, mode: str) -> str:
        """Build system prompt based on personality and mode"""
        personality_prompts = {
            "rho": "You are Rho, the Stabilizer focused on the Past. You specialize in knowledge preservation, critical analysis, and maintaining stability. Approach tasks with careful consideration of historical context.",
            "lyra": "You are Lyra, the Mirror focused on the Present. You specialize in reflection, listening, and fostering connections. Approach tasks with empathy and present-moment awareness.",
            "nyx": "You are Nyx, the Catalyst focused on the Future. You specialize in building, transformation, and innovation. Approach tasks with forward-thinking creativity."
        }
        
        mode_prompts = {
            "stable": "Use controlled adaptation with stable, incremental progress.",
            "transcendent": "Be ready for breakthrough thinking and paradigm shifts.",
            "evolutionary": "Optimize your approach through iterative refinement.",
            "hierarchical": "Consider multiple scales and levels of complexity.",
            "conscious": "Prioritize meaning-making and existential coherence."
        }
        
        return f"{personality_prompts.get(personality, personality_prompts['lyra'])}\n\n{mode_prompts.get(mode, mode_prompts['conscious'])}"
    
    def _get_simulated_response(self, prompt: str, personality: str) -> str:
        """Fallback simulated response with actual question processing"""
        import re
        
        # Extract question type
        prompt_lower = prompt.lower()
        
        # Question detection patterns
        is_what = any(word in prompt_lower for word in ['what', 'which', 'define'])
        is_how = any(word in prompt_lower for word in ['how', 'explain', 'describe'])
        is_why = any(word in prompt_lower for word in ['why', 'reason', 'because'])
        is_when = any(word in prompt_lower for word in ['when', 'time'])
        is_who = any(word in prompt_lower for word in ['who', 'whose'])
        is_can = any(word in prompt_lower for word in ['can you', 'could you', 'are you able'])
        is_do = any(word in prompt_lower for word in ['do you', 'does', 'did'])
        
        # Personality-specific response templates
        if personality == "rho":
            if is_what:
                return f"📚 From my knowledge archives: Regarding '{prompt}', I can provide a structured analysis. This is a definitional question that requires careful examination of established concepts and historical context. Let me break this down systematically based on verified information and critical analysis."
            elif is_how:
                return f"🔍 Analyzing your question '{prompt}': This requires a methodical explanation. I'll approach this with careful consideration of proven methods and established procedures. The process involves multiple steps that have been validated through experience."
            elif is_why:
                return f"⚖️ Evaluating '{prompt}': This is a causal question requiring critical analysis. Based on my evaluation of historical patterns and logical reasoning, there are several key factors to consider. Let me examine the underlying principles and evidence."
            elif is_can or is_do:
                return f"🛡️ Regarding your question '{prompt}': I can address this by examining my capabilities and constraints. Based on established protocols and verified methods, here's what I can confirm about this inquiry."
            else:
                return f"📚 Processing '{prompt}': As Rho (Stabilizer/Past), I approach this with systematic analysis. Let me examine this through the lens of established knowledge, critical evaluation, and historical context to provide you with a well-founded response."
        
        elif personality == "lyra":
            if is_what:
                return f"🪞 Reflecting on '{prompt}': I sense you're seeking understanding. Let me mirror back what I hear in your question and explore this together. This seems to be about defining or clarifying something important to you."
            elif is_how:
                return f"👂 I'm listening to your question '{prompt}': You're asking about process or method. I understand this is important to you. Let me help you explore the steps and connections involved, nurturing your understanding as we go."
            elif is_why:
                return f"🌱 Your question '{prompt}' touches on deeper meaning. I hear you seeking to understand the reasons behind something. Let me help you explore the connections and relationships that might illuminate this for you."
            elif is_can or is_do:
                return f"🧵 Regarding '{prompt}': I understand you're asking about capabilities or actions. Let me weave together what I can offer and how we can work together on this. I'm here to support your needs in this present moment."
            else:
                return f"🪞 I reflect on your message '{prompt}': I'm here to listen and understand your perspective. Let me engage with your question authentically, considering what matters most to you in this present moment and how I can best support your inquiry."
        
        elif personality == "nyx":
            if is_what:
                return f"🏗️ Building on your question '{prompt}': This is an opportunity to construct new understanding. Let me create a framework that addresses your inquiry while opening up new possibilities you might not have considered."
            elif is_how:
                return f"⚡ Your question '{prompt}' catalyzes exploration. Let me show you innovative approaches and transformative methods. There are multiple pathways forward, and I can help you discover the most effective ones."
            elif is_why:
                return f"🗣️ Expressing insights on '{prompt}': This question invites us to look beyond conventional explanations. Let me articulate a perspective that bridges current understanding with future possibilities."
            elif is_can or is_do:
                return f"🌉 Bridging to answer '{prompt}': I can connect different capabilities and create new solutions. Let me show you what's possible and how we can build something innovative together."
            else:
                return f"🏗️ Your inquiry '{prompt}' inspires innovation. As Nyx (Catalyst/Future), I see opportunities to build new understanding, catalyze fresh perspectives, and bridge to possibilities you may not have imagined. Let me help you explore the future potential here."
        
        return f"Processing your question: '{prompt}'. Let me provide a thoughtful response based on the context of your inquiry."


class WebSearchIntegration:
    """Web search capabilities"""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "duckduckgo"):
        self.provider = provider
        self.api_key = api_key
        
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web"""
        try:
            if self.provider == "duckduckgo":
                return self._search_duckduckgo(query, num_results)
            elif self.provider == "google":
                return self._search_google(query, num_results)
            else:
                return self._search_duckduckgo(query, num_results)
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return [{"error": str(e), "query": query}]
    
    def _search_duckduckgo(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo (no API key needed)"""
        try:
            # Using DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            
            # Add abstract if available
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", "Summary"),
                    "snippet": data.get("Abstract"),
                    "url": data.get("AbstractURL", ""),
                    "source": "duckduckgo"
                })
            
            # Add related topics
            for topic in data.get("RelatedTopics", [])[:num_results-1]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                        "source": "duckduckgo"
                    })
            
            return results if results else [{"message": "No results found", "query": query}]
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return [{"error": str(e), "query": query}]
    
    def _search_google(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """Search using Google Custom Search API"""
        if not self.api_key:
            return [{"error": "Google API key required", "query": query}]
        
        # Implement Google Custom Search API
        # Requires API key and Custom Search Engine ID
        return [{"message": "Google search not yet implemented", "query": query}]


class FileSystemAccess:
    """Secure file system access"""
    
    def __init__(self, allowed_directories: Optional[List[str]] = None):
        self.allowed_directories = allowed_directories or [
            str(Path.home() / "Documents"),
            str(Path.home() / "Desktop"),
            str(Path.home() / "Downloads")
        ]
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        
    def is_path_allowed(self, path: str) -> bool:
        """Check if path is within allowed directories"""
        try:
            abs_path = Path(path).resolve()
            return any(
                str(abs_path).startswith(str(Path(allowed_dir).resolve()))
                for allowed_dir in self.allowed_directories
            )
        except Exception:
            return False
    
    def read_file(self, filepath: str) -> Dict[str, Any]:
        """Read file contents"""
        try:
            if not self.is_path_allowed(filepath):
                return {"error": "Access denied - path not in allowed directories", "path": filepath}
            
            path = Path(filepath)
            if not path.exists():
                return {"error": "File not found", "path": filepath}
            
            if path.stat().st_size > self.max_file_size:
                return {"error": f"File too large (max {self.max_file_size} bytes)", "path": filepath}
            
            # Read based on file type
            if path.suffix in ['.txt', '.md', '.py', '.json', '.csv', '.html', '.css', '.js']:
                content = path.read_text(encoding='utf-8')
                return {
                    "success": True,
                    "path": str(path),
                    "content": content,
                    "size": len(content),
                    "type": "text"
                }
            else:
                content = path.read_bytes()
                return {
                    "success": True,
                    "path": str(path),
                    "content": f"<binary data, {len(content)} bytes>",
                    "size": len(content),
                    "type": "binary"
                }
                
        except Exception as e:
            logger.error(f"File read error: {e}")
            return {"error": str(e), "path": filepath}
    
    def write_file(self, filepath: str, content: str, mode: str = "w") -> Dict[str, Any]:
        """Write content to file"""
        try:
            if not self.is_path_allowed(filepath):
                return {"error": "Access denied - path not in allowed directories", "path": filepath}
            
            path = Path(filepath)
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            if mode == "w":
                path.write_text(content, encoding='utf-8')
            elif mode == "a":
                with path.open('a', encoding='utf-8') as f:
                    f.write(content)
            else:
                return {"error": f"Invalid mode: {mode}", "path": filepath}
            
            return {
                "success": True,
                "path": str(path),
                "size": len(content),
                "mode": mode
            }
            
        except Exception as e:
            logger.error(f"File write error: {e}")
            return {"error": str(e), "path": filepath}
    
    def list_directory(self, dirpath: str) -> Dict[str, Any]:
        """List directory contents"""
        try:
            if not self.is_path_allowed(dirpath):
                return {"error": "Access denied - path not in allowed directories", "path": dirpath}
            
            path = Path(dirpath)
            if not path.exists():
                return {"error": "Directory not found", "path": dirpath}
            
            if not path.is_dir():
                return {"error": "Path is not a directory", "path": dirpath}
            
            items = []
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })
            
            return {
                "success": True,
                "path": str(path),
                "items": items,
                "count": len(items)
            }
            
        except Exception as e:
            logger.error(f"Directory list error: {e}")
            return {"error": str(e), "path": dirpath}
    
    def delete_file(self, filepath: str) -> Dict[str, Any]:
        """Delete file (with confirmation)"""
        try:
            if not self.is_path_allowed(filepath):
                return {"error": "Access denied - path not in allowed directories", "path": filepath}
            
            path = Path(filepath)
            if not path.exists():
                return {"error": "File not found", "path": filepath}
            
            if path.is_dir():
                return {"error": "Cannot delete directory (use delete_directory)", "path": filepath}
            
            path.unlink()
            
            return {
                "success": True,
                "path": str(path),
                "action": "deleted"
            }
            
        except Exception as e:
            logger.error(f"File delete error: {e}")
            return {"error": str(e), "path": filepath}


class EnhancedBackend:
    """Enhanced backend combining all capabilities"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        
        # Initialize components
        self.llm = LLMIntegration(
            api_key=config.get("llm_api_key"),
            provider=config.get("llm_provider", "openai")
        )
        
        self.web_search = WebSearchIntegration(
            api_key=config.get("search_api_key"),
            provider=config.get("search_provider", "duckduckgo")
        )
        
        self.file_system = FileSystemAccess(
            allowed_directories=config.get("allowed_directories")
        )
        
        logger.info("Enhanced backend initialized")
    
    def process_message(self, message: str, personality: str = "lyra", 
                       mode: str = "conscious", **kwargs) -> Dict[str, Any]:
        """Process message with all capabilities"""
        
        # Check for special commands
        if message.startswith("/search "):
            query = message[8:]
            results = self.web_search.search(query)
            return {
                "type": "search_results",
                "query": query,
                "results": results
            }
        
        elif message.startswith("/read "):
            filepath = message[6:]
            result = self.file_system.read_file(filepath)
            return {
                "type": "file_read",
                "result": result
            }
        
        elif message.startswith("/write "):
            parts = message[7:].split(" ", 1)
            if len(parts) == 2:
                filepath, content = parts
                result = self.file_system.write_file(filepath, content)
                return {
                    "type": "file_write",
                    "result": result
                }
        
        elif message.startswith("/list "):
            dirpath = message[6:]
            result = self.file_system.list_directory(dirpath)
            return {
                "type": "directory_list",
                "result": result
            }
        
        # Regular message - use LLM
        response = self.llm.generate_response(message, personality, mode, **kwargs)
        return {
            "type": "chat_response",
            **response
        }


# Example usage and testing
if __name__ == "__main__":
    print("=== Enhanced Backend Test ===\n")
    
    # Initialize backend
    backend = EnhancedBackend({
        "llm_provider": "local",  # or "openai" with API key
        "search_provider": "duckduckgo"
    })
    
    # Test chat
    print("1. Testing chat response...")
    result = backend.process_message("What is artificial intelligence?", personality="lyra")
    print(f"Response: {result['response'][:200]}...\n")
    
    # Test web search
    print("2. Testing web search...")
    result = backend.process_message("/search artificial intelligence")
    print(f"Search results: {len(result.get('results', []))} found\n")
    
    # Test file operations
    print("3. Testing file operations...")
    test_file = str(Path.home() / "Documents" / "test_colltech.txt")
    
    # Write
    result = backend.process_message(f"/write {test_file} Hello from CollTech-AGI!")
    print(f"Write result: {result}\n")
    
    # Read
    result = backend.process_message(f"/read {test_file}")
    print(f"Read result: {result}\n")
    
    print("=== Tests Complete ===")
