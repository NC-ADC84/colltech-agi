#!/usr/bin/env python3
"""
Web API Example - CollTech-AGI Framework

An example showing how to create a web API using FastAPI
with CollTech-AGI integration.
"""

import sys
import os
import asyncio
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("❌ FastAPI not installed. Install with: pip install fastapi uvicorn")
    sys.exit(1)

from colltech_agi_framework import CollTechAGIAdvanced, FrameworkConfig
from colltech_agi_personality_system import PersonalityProfile

# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    personality: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    personality: str
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    interaction_id: int
    timestamp: float

class PersonalityRequest(BaseModel):
    personality: str

class PersonalityResponse(BaseModel):
    success: bool
    message: str
    current_personality: str

class StatusResponse(BaseModel):
    is_running: bool
    uptime_seconds: float
    interaction_count: int
    current_personality: str
    intelligent_personality_enabled: bool
    catalyst_integration_enabled: bool
    advanced_features: Dict[str, bool]

# Initialize FastAPI app
app = FastAPI(
    title="CollTech-AGI Web API",
    description="A consciousness-based AI with personality system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CollTech-AGI
config = FrameworkConfig(
    auto_personality_enabled=True,
    catalyst_integration_enabled=True,
    debug_mode=False
)
agi = CollTechAGIAdvanced(config)
agi.start()

print("🚀 CollTech-AGI Web API initialized")

@app.on_event("startup")
async def startup_event():
    """Called when the API starts up."""
    print("✅ CollTech-AGI Web API started")

@app.on_event("shutdown")
async def shutdown_event():
    """Called when the API shuts down."""
    agi.shutdown()
    print("🛑 CollTech-AGI Web API shutdown")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CollTech-AGI Web API",
        "version": "1.0.0",
        "description": "A consciousness-based AI with personality system",
        "endpoints": {
            "chat": "/chat",
            "personality": "/personality",
            "status": "/status",
            "docs": "/docs"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with CollTech-AGI."""
    try:
        # Set personality if specified
        if request.personality:
            if request.personality.lower() in ['rho', 'lyra', 'nyx']:
                agi.personality_system.set_profile(PersonalityProfile(request.personality.lower()))
            else:
                raise HTTPException(status_code=400, detail="Invalid personality. Use: rho, lyra, or nyx")
        
        # Process input
        result = agi.process_input(request.message)
        
        return ChatResponse(
            response=result['response'],
            personality=result['personality']['selected_profile'],
            confidence=result['personality'].get('confidence'),
            reasoning=result['personality'].get('reasoning'),
            interaction_id=result['interaction_id'],
            timestamp=result['timestamp']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personality")
async def get_personality():
    """Get current personality information."""
    try:
        info = agi.get_personality_info()
        return {
            "current_profile": info['current_profile'],
            "description": info['description'],
            "dominant_attributes": info['dominant_attributes'],
            "available_profiles": info['available_profiles']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/personality", response_model=PersonalityResponse)
async def set_personality(request: PersonalityRequest):
    """Set personality profile."""
    try:
        if request.personality.lower() not in ['rho', 'lyra', 'nyx']:
            raise HTTPException(status_code=400, detail="Invalid personality. Use: rho, lyra, or nyx")
        
        success = agi.set_personality(request.personality.lower())
        
        if success:
            return PersonalityResponse(
                success=True,
                message=f"Personality set to {request.personality.title()}",
                current_personality=agi.get_personality()
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to set personality")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status."""
    try:
        status = agi.get_advanced_status()
        return StatusResponse(
            is_running=status['is_running'],
            uptime_seconds=status['uptime_seconds'],
            interaction_count=status['interaction_count'],
            current_personality=status['current_personality'],
            intelligent_personality_enabled=status['intelligent_personality']['enabled'],
            catalyst_integration_enabled=status['catalyst_integration']['enabled'],
            advanced_features=status['advanced_features']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/intelligent-personality")
async def get_intelligent_personality_status():
    """Get intelligent personality selection status."""
    try:
        return {
            "enabled": agi.config.auto_personality_enabled,
            "interaction_history_count": len(agi.intelligent_selector.interaction_history),
            "learned_preferences_count": len(agi.intelligent_selector.user_preferences)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/intelligent-personality")
async def toggle_intelligent_personality(enabled: bool):
    """Toggle intelligent personality selection."""
    try:
        if enabled:
            agi.enable_intelligent_personality()
        else:
            agi.disable_intelligent_personality()
        
        return {
            "success": True,
            "message": f"Intelligent personality selection {'enabled' if enabled else 'disabled'}",
            "enabled": agi.config.auto_personality_enabled
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/selection-history")
async def get_selection_history():
    """Get personality selection history."""
    try:
        history = agi.get_selection_history()
        return {
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learned-preferences")
async def get_learned_preferences():
    """Get learned user preferences."""
    try:
        preferences = agi.get_learned_preferences()
        return {
            "preferences": preferences,
            "count": len(preferences)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset-preferences")
async def reset_learned_preferences():
    """Reset learned user preferences."""
    try:
        agi.reset_learned_preferences()
        return {
            "success": True,
            "message": "Learned preferences reset"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/catalyst-status")
async def get_catalyst_status():
    """Get catalyst integration protocol status."""
    try:
        cip_status = agi.get_catalyst_status()
        return cip_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/catalyst-pair")
async def pair_catalyst_with_stabilizer(stabilizer: str):
    """Pair catalyst with stabilizer."""
    try:
        if stabilizer.lower() not in ['rho', 'lyra']:
            raise HTTPException(status_code=400, detail="Invalid stabilizer. Use: rho or lyra")
        
        result = agi.pair_catalyst_with_stabilizer(stabilizer.lower())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/catalyst-elevate")
async def elevate_catalyst():
    """Attempt to elevate catalyst."""
    try:
        result = agi.elevate_catalyst()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """Main function to run the web API."""
    print("🚀 Starting CollTech-AGI Web API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 API Endpoints: http://localhost:8000")
    print("=" * 50)
    
    # Run the API
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()
