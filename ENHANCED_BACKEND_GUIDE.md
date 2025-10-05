# CollTech-AGI Enhanced Backend Guide

## 🚀 Overview

The Enhanced Backend adds three major capabilities to CollTech-AGI:
1. **LLM API Integration** - Connect to OpenAI, Anthropic, or local LLMs
2. **Web Search** - Search the internet using DuckDuckGo (no API key needed)
3. **File System Access** - Securely read, write, and manage files

## 📋 Features

### 1. LLM Integration

Connect to real AI models instead of simulated responses.

**Supported Providers:**
- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude 3)
- **Local LLM** (Ollama, LM Studio)

**Configuration:**

```bash
# For OpenAI
set OPENAI_API_KEY=your-api-key-here
set LLM_PROVIDER=openai

# For Anthropic
set ANTHROPIC_API_KEY=your-api-key-here
set LLM_PROVIDER=anthropic

# For Local LLM (Ollama)
set LLM_PROVIDER=local
# Make sure Ollama is running on localhost:11434
```

### 2. Web Search

Search the web directly from the chat interface.

**Features:**
- No API key required (uses DuckDuckGo)
- Returns instant answers and related topics
- Integrated into chat UI with `/search` command

**Usage:**
```
/search artificial intelligence
/search Python programming tutorial
/search latest news on quantum computing
```

### 3. File System Access

Securely read, write, and manage files on your computer.

**Security Features:**
- Restricted to allowed directories (Documents, Desktop, Downloads by default)
- 10MB file size limit
- Access control validation
- Safe file operations

**Commands:**

```bash
# Read a file
/read C:/Users/Andre/Documents/myfile.txt

# Write to a file
/write C:/Users/Andre/Documents/note.txt Hello World!

# List directory contents
/list C:/Users/Andre/Documents

# Get help
/help
```

## 🔧 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install requests
```

### Step 2: Configure API Keys (Optional)

For OpenAI:
```bash
# Windows
set OPENAI_API_KEY=sk-your-key-here

# Linux/Mac
export OPENAI_API_KEY=sk-your-key-here
```

For Anthropic:
```bash
# Windows
set ANTHROPIC_API_KEY=your-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-key-here
```

### Step 3: Configure Allowed Directories (Optional)

Edit `colltech_agi_enhanced_backend.py` to customize allowed directories:

```python
self.allowed_directories = [
    str(Path.home() / "Documents"),
    str(Path.home() / "Desktop"),
    str(Path.home() / "Downloads"),
    # Add more directories as needed
]
```

### Step 4: Launch Enhanced Chat UI

```bash
cd colltech-agi
python colltech_agi_chat_ui.py
```

## 💻 Usage Examples

### Example 1: Web Research

```
You: /search latest developments in AI
System: Searching for: latest developments in AI
System: Found 5 results:
System: 1. Recent AI Breakthroughs
System:    Major advances in large language models...
```

### Example 2: File Management

```
You: /list C:/Users/Andre/Documents
System: Listing directory: C:/Users/Andre/Documents
System: Found 15 items:
System: 📄 report.docx
System: 📁 Projects
System: 📄 notes.txt
```

### Example 3: Reading Files

```
You: /read C:/Users/Andre/Documents/notes.txt
System: Reading file: C:/Users/Andre/Documents/notes.txt
System: File content (245 bytes):
CollTech-AGI: [Content of the file displayed here]
```

### Example 4: Writing Files

```
You: /write C:/Users/Andre/Documents/todo.txt Buy groceries, Call dentist
System: Writing file...
System: File written successfully: C:/Users/Andre/Documents/todo.txt
```

### Example 5: Natural Conversation with LLM

```
You: What is the meaning of consciousness?
CollTech-AGI (lyra): [Thoughtful response from actual LLM or simulated personality]
Source: openai
📊 Meaning: 0.85 | Existential: 0.92 | Chapter: exploring_identity
```

## 🔒 Security

### Access Control

Files can only be accessed in allowed directories:
- ✅ `C:/Users/Andre/Documents`
- ✅ `C:/Users/Andre/Desktop`
- ✅ `C:/Users/Andre/Downloads`
- ❌ `C:/Windows/System32` (blocked)
- ❌ `C:/Program Files` (blocked)

### File Size Limits

- Maximum file size: 10MB
- Prevents memory issues with large files
- Configurable in backend settings

### Safe Operations

- All file paths are validated
- Directory traversal attacks prevented
- Error handling for all operations
- No execution of arbitrary code

## 🧪 Testing

Run the test suite:

```bash
cd colltech-agi
python test_enhanced_backend.py
```

**Test Coverage:**
- ✅ Web search functionality
- ✅ File read/write/list operations
- ✅ LLM integration (all providers)
- ✅ Personality and mode switching
- ✅ Security controls

## 🎯 Advanced Configuration

### Custom LLM Models

Edit `colltech_agi_enhanced_backend.py`:

```python
# For OpenAI
data = {
    "model": "gpt-4-turbo-preview",  # Change model here
    ...
}

# For Anthropic
data = {
    "model": "claude-3-opus-20240229",  # Change model here
    ...
}

# For Local (Ollama)
data = {
    "model": "llama2",  # or "mistral", "codellama", etc.
    ...
}
```

### Custom Search Provider

To use Google Custom Search instead of DuckDuckGo:

```python
backend = EnhancedBackend({
    "search_provider": "google",
    "search_api_key": "your-google-api-key",
    "search_engine_id": "your-search-engine-id"
})
```

### Extend Allowed Directories

```python
backend = EnhancedBackend({
    "allowed_directories": [
        "C:/Users/Andre/Documents",
        "C:/Users/Andre/Projects",
        "D:/Data"  # Add custom directories
    ]
})
```

## 📊 Performance

- **Web Search**: ~1-3 seconds per query
- **File Operations**: <100ms for files under 1MB
- **LLM Responses**: 
  - OpenAI: 2-10 seconds
  - Anthropic: 2-8 seconds
  - Local: 5-30 seconds (depends on hardware)

## 🐛 Troubleshooting

### Issue: "No API key" error

**Solution:** Set environment variable:
```bash
set OPENAI_API_KEY=your-key-here
```

### Issue: "Access denied" for file operations

**Solution:** File must be in allowed directory. Check:
```python
# Allowed by default:
C:/Users/Andre/Documents
C:/Users/Andre/Desktop
C:/Users/Andre/Downloads
```

### Issue: Web search returns no results

**Solution:** 
- Check internet connection
- DuckDuckGo API may be rate-limited
- Try again in a few seconds

### Issue: Local LLM not connecting

**Solution:**
- Install Ollama: https://ollama.ai
- Start Ollama: `ollama serve`
- Pull a model: `ollama pull llama2`
- Verify running: http://localhost:11434

## 🔄 Fallback Behavior

If enhanced features are unavailable, the system gracefully falls back:

1. **No LLM API**: Uses simulated personality responses
2. **No Web Search**: Shows "not available" message
3. **No File Access**: Shows "not available" message

The chat UI always works, even without enhanced features!

## 📚 API Reference

### EnhancedBackend Class

```python
from colltech_agi_enhanced_backend import EnhancedBackend

# Initialize
backend = EnhancedBackend({
    "llm_provider": "openai",  # or "anthropic", "local"
    "llm_api_key": "your-key",
    "search_provider": "duckduckgo",
    "allowed_directories": [...]
})

# Process message
result = backend.process_message(
    message="Your message",
    personality="lyra",  # or "rho", "nyx"
    mode="conscious"  # or "stable", "transcendent", etc.
)
```

### LLMIntegration Class

```python
from colltech_agi_enhanced_backend import LLMIntegration

llm = LLMIntegration(api_key="your-key", provider="openai")
response = llm.generate_response(
    prompt="Your prompt",
    personality="lyra",
    mode="conscious"
)
```

### WebSearchIntegration Class

```python
from colltech_agi_enhanced_backend import WebSearchIntegration

search = WebSearchIntegration(provider="duckduckgo")
results = search.search(query="AI research", num_results=5)
```

### FileSystemAccess Class

```python
from colltech_agi_enhanced_backend import FileSystemAccess

fs = FileSystemAccess(allowed_directories=[...])

# Read
result = fs.read_file("path/to/file.txt")

# Write
result = fs.write_file("path/to/file.txt", "content")

# List
result = fs.list_directory("path/to/directory")
```

## 🎓 Best Practices

1. **API Keys**: Store in environment variables, never in code
2. **File Paths**: Always use absolute paths for clarity
3. **Error Handling**: Check result['success'] before using data
4. **Rate Limiting**: Don't spam web searches (respect API limits)
5. **File Sizes**: Keep files under 10MB for best performance
6. **Security**: Only allow necessary directories

## 🚀 Next Steps

1. **Get API Keys**: Sign up for OpenAI or Anthropic
2. **Install Ollama**: For free local LLM option
3. **Test Features**: Run `test_enhanced_backend.py`
4. **Customize**: Adjust settings for your needs
5. **Explore**: Try different personalities and modes!

## 📞 Support

For issues or questions:
1. Check this guide
2. Review test output
3. Check error messages in chat UI
4. Verify API keys and configuration

---

**Version**: 2.0.0 (Enhanced)  
**Last Updated**: 2024  
**Status**: ✅ Fully Operational
