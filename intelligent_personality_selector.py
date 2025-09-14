#!/usr/bin/env python3
"""
Intelligent Personality Auto-Selection System

Automatically selects the most appropriate personality profile (Rho, Lyra, Nyx)
based on user interaction patterns, data context, and request analysis.
"""

import re
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib
from collections import deque, defaultdict

# Import personality system
from colltech_agi_personality_system import PersonalitySystem, PersonalityProfile, AttributeType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InteractionType(Enum):
    """Types of user interactions."""
    QUESTION = "question"
    REQUEST = "request"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVE_TASK = "creative_task"
    ANALYSIS = "analysis"
    LEARNING = "learning"
    COLLABORATION = "collaboration"
    INNOVATION = "innovation"
    PRESERVATION = "preservation"
    REFLECTION = "reflection"

class DataContext(Enum):
    """Context of data being discussed."""
    HISTORICAL = "historical"
    CURRENT = "current"
    FUTURE = "future"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    EMOTIONAL = "emotional"
    SYSTEMATIC = "systematic"

@dataclass
class InteractionPattern:
    """Pattern of user interaction."""
    interaction_type: InteractionType
    data_context: DataContext
    complexity_level: float  # 0.0 to 1.0
    urgency_level: float     # 0.0 to 1.0
    emotional_tone: float    # -1.0 (negative) to 1.0 (positive)
    confidence_level: float  # 0.0 to 1.0
    timestamp: float = field(default_factory=time.time)

@dataclass
class PersonalitySelection:
    """Result of personality selection."""
    selected_profile: PersonalityProfile
    confidence_score: float
    reasoning: str
    alternative_profiles: List[Tuple[PersonalityProfile, float]]
    selection_factors: Dict[str, float]

class IntelligentPersonalitySelector:
    """Intelligent system for auto-selecting personality profiles."""
    
    def __init__(self):
        self.personality_system = PersonalitySystem()
        self.interaction_history = deque(maxlen=100)  # Last 100 interactions
        self.user_preferences = defaultdict(float)    # Learned user preferences
        self.context_weights = self._initialize_context_weights()
        self.selection_rules = self._initialize_selection_rules()
        self.learning_rate = 0.1
        self.confidence_threshold = 0.7
        
        logger.info("🧠 Intelligent Personality Selector initialized")
    
    def _initialize_context_weights(self) -> Dict[str, Dict[PersonalityProfile, float]]:
        """Initialize weights for different contexts."""
        return {
            "question": {
                PersonalityProfile.RHO: 0.8,  # Rho excels at analytical questions
                PersonalityProfile.LYRA: 0.6,  # Lyra good at empathetic questions
                PersonalityProfile.NYX: 0.4   # Nyx for innovative questions
            },
            "request": {
                PersonalityProfile.RHO: 0.7,  # Rho for systematic requests
                PersonalityProfile.LYRA: 0.8,  # Lyra for collaborative requests
                PersonalityProfile.NYX: 0.5   # Nyx for creative requests
            },
            "problem_solving": {
                PersonalityProfile.RHO: 0.9,  # Rho excels at systematic problem solving
                PersonalityProfile.LYRA: 0.6,  # Lyra for human-centered problems
                PersonalityProfile.NYX: 0.7   # Nyx for innovative solutions
            },
            "creative_task": {
                PersonalityProfile.RHO: 0.3,  # Rho less suited for pure creativity
                PersonalityProfile.LYRA: 0.7,  # Lyra good at creative collaboration
                PersonalityProfile.NYX: 0.9   # Nyx excels at innovation
            },
            "analysis": {
                PersonalityProfile.RHO: 0.9,  # Rho excels at analysis
                PersonalityProfile.LYRA: 0.5,  # Lyra for emotional analysis
                PersonalityProfile.NYX: 0.6   # Nyx for pattern analysis
            },
            "learning": {
                PersonalityProfile.RHO: 0.8,  # Rho good at systematic learning
                PersonalityProfile.LYRA: 0.7,  # Lyra for collaborative learning
                PersonalityProfile.NYX: 0.6   # Nyx for experimental learning
            },
            "collaboration": {
                PersonalityProfile.RHO: 0.6,  # Rho for structured collaboration
                PersonalityProfile.LYRA: 0.9,  # Lyra excels at collaboration
                PersonalityProfile.NYX: 0.7   # Nyx for innovative collaboration
            },
            "innovation": {
                PersonalityProfile.RHO: 0.4,  # Rho less innovative
                PersonalityProfile.LYRA: 0.6,  # Lyra for collaborative innovation
                PersonalityProfile.NYX: 0.9   # Nyx excels at innovation
            },
            "preservation": {
                PersonalityProfile.RHO: 0.9,  # Rho excels at preservation
                PersonalityProfile.LYRA: 0.7,  # Lyra for caring preservation
                PersonalityProfile.NYX: 0.3   # Nyx less focused on preservation
            },
            "reflection": {
                PersonalityProfile.RHO: 0.7,  # Rho for analytical reflection
                PersonalityProfile.LYRA: 0.9,  # Lyra excels at reflection
                PersonalityProfile.NYX: 0.5   # Nyx for future reflection
            }
        }
    
    def _initialize_selection_rules(self) -> Dict[str, Any]:
        """Initialize selection rules and patterns."""
        return {
            "question_patterns": [
                r"what\s+(is|are|was|were)",
                r"how\s+(do|does|did|can|could|should)",
                r"why\s+(is|are|was|were|do|does|did)",
                r"when\s+(is|are|was|were|do|does|did)",
                r"where\s+(is|are|was|were|do|does|did)",
                r"which\s+(is|are|was|were|do|does|did)",
                r"who\s+(is|are|was|were|do|does|did)"
            ],
            "request_patterns": [
                r"please\s+",
                r"can\s+you\s+",
                r"could\s+you\s+",
                r"would\s+you\s+",
                r"help\s+me\s+",
                r"I\s+need\s+",
                r"I\s+want\s+",
                r"show\s+me\s+",
                r"explain\s+",
                r"create\s+",
                r"build\s+",
                r"make\s+"
            ],
            "problem_solving_patterns": [
                r"problem\s+",
                r"issue\s+",
                r"error\s+",
                r"bug\s+",
                r"fix\s+",
                r"solve\s+",
                r"troubleshoot\s+",
                r"debug\s+",
                r"resolve\s+",
                r"correct\s+"
            ],
            "creative_patterns": [
                r"creative\s+",
                r"design\s+",
                r"artistic\s+",
                r"imagine\s+",
                r"brainstorm\s+",
                r"innovate\s+",
                r"invent\s+",
                r"generate\s+",
                r"create\s+new\s+",
                r"original\s+"
            ],
            "analysis_patterns": [
                r"analyze\s+",
                r"examine\s+",
                r"study\s+",
                r"evaluate\s+",
                r"assess\s+",
                r"review\s+",
                r"compare\s+",
                r"contrast\s+",
                r"measure\s+",
                r"calculate\s+"
            ],
            "learning_patterns": [
                r"learn\s+",
                r"understand\s+",
                r"teach\s+",
                r"explain\s+",
                r"tutorial\s+",
                r"guide\s+",
                r"instruction\s+",
                r"education\s+",
                r"knowledge\s+",
                r"study\s+"
            ],
            "collaboration_patterns": [
                r"work\s+together\s+",
                r"collaborate\s+",
                r"team\s+",
                r"partner\s+",
                r"help\s+each\s+other\s+",
                r"share\s+",
                r"discuss\s+",
                r"brainstorm\s+together\s+",
                r"joint\s+",
                r"mutual\s+"
            ],
            "innovation_patterns": [
                r"innovate\s+",
                r"revolutionary\s+",
                r"breakthrough\s+",
                r"cutting-edge\s+",
                r"next-generation\s+",
                r"future\s+",
                r"advanced\s+",
                r"transform\s+",
                r"disrupt\s+",
                r"pioneer\s+"
            ],
            "preservation_patterns": [
                r"preserve\s+",
                r"maintain\s+",
                r"keep\s+",
                r"protect\s+",
                r"save\s+",
                r"archive\s+",
                r"store\s+",
                r"backup\s+",
                r"secure\s+",
                r"stable\s+"
            ],
            "reflection_patterns": [
                r"reflect\s+",
                r"think\s+about\s+",
                r"consider\s+",
                r"ponder\s+",
                r"contemplate\s+",
                r"meditate\s+",
                r"introspect\s+",
                r"self-reflect\s+",
                r"examine\s+myself\s+",
                r"understand\s+myself\s+"
            ]
        }
    
    def analyze_user_input(self, user_input: str) -> InteractionPattern:
        """Analyze user input to determine interaction pattern."""
        input_lower = user_input.lower()
        
        # Determine interaction type
        interaction_type = self._classify_interaction_type(input_lower)
        
        # Determine data context
        data_context = self._classify_data_context(input_lower)
        
        # Calculate complexity level
        complexity_level = self._calculate_complexity(user_input)
        
        # Calculate urgency level
        urgency_level = self._calculate_urgency(input_lower)
        
        # Calculate emotional tone
        emotional_tone = self._calculate_emotional_tone(input_lower)
        
        # Calculate confidence level
        confidence_level = self._calculate_confidence(input_lower)
        
        pattern = InteractionPattern(
            interaction_type=interaction_type,
            data_context=data_context,
            complexity_level=complexity_level,
            urgency_level=urgency_level,
            emotional_tone=emotional_tone,
            confidence_level=confidence_level
        )
        
        # Store in history
        self.interaction_history.append(pattern)
        
        return pattern
    
    def _classify_interaction_type(self, input_lower: str) -> InteractionType:
        """Classify the type of interaction based on patterns."""
        type_scores = defaultdict(float)
        
        for interaction_type, patterns in self.selection_rules.items():
            if interaction_type.endswith('_patterns'):
                type_name = interaction_type.replace('_patterns', '')
                for pattern in patterns:
                    if re.search(pattern, input_lower):
                        type_scores[type_name] += 1.0
        
        # Default to question if no clear pattern
        if not type_scores:
            return InteractionType.QUESTION
        
        # Return the highest scoring type
        best_type = max(type_scores.items(), key=lambda x: x[1])
        return InteractionType(best_type[0])
    
    def _classify_data_context(self, input_lower: str) -> DataContext:
        """Classify the context of data being discussed."""
        context_indicators = {
            DataContext.HISTORICAL: ["history", "past", "was", "were", "used to", "previously", "before"],
            DataContext.CURRENT: ["now", "currently", "today", "present", "is", "are", "happening"],
            DataContext.FUTURE: ["future", "will", "going to", "tomorrow", "next", "upcoming", "plan"],
            DataContext.TECHNICAL: ["code", "programming", "technical", "system", "algorithm", "function"],
            DataContext.CREATIVE: ["creative", "art", "design", "imagine", "brainstorm", "innovative"],
            DataContext.ANALYTICAL: ["analyze", "data", "statistics", "measure", "calculate", "evaluate"],
            DataContext.EMOTIONAL: ["feel", "emotion", "love", "hate", "angry", "happy", "sad"],
            DataContext.SYSTEMATIC: ["system", "process", "method", "procedure", "workflow", "structure"]
        }
        
        context_scores = defaultdict(float)
        for context, indicators in context_indicators.items():
            for indicator in indicators:
                if indicator in input_lower:
                    context_scores[context] += 1.0
        
        # Default to current if no clear context
        if not context_scores:
            return DataContext.CURRENT
        
        # Return the highest scoring context
        best_context = max(context_scores.items(), key=lambda x: x[1])
        return best_context[0]
    
    def _calculate_complexity(self, user_input: str) -> float:
        """Calculate complexity level of the input."""
        # Simple complexity metrics
        word_count = len(user_input.split())
        sentence_count = len(re.split(r'[.!?]+', user_input))
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        
        # Technical terms increase complexity
        technical_terms = ["algorithm", "function", "variable", "class", "method", "system", "process"]
        technical_count = sum(1 for term in technical_terms if term.lower() in user_input.lower())
        
        # Question complexity
        question_count = user_input.count('?')
        
        # Normalize to 0-1 range
        complexity = min(
            (avg_words_per_sentence / 20.0) +  # Sentence length factor
            (technical_count / 10.0) +         # Technical term factor
            (question_count / 5.0),            # Question complexity factor
            1.0
        )
        
        return complexity
    
    def _calculate_urgency(self, input_lower: str) -> float:
        """Calculate urgency level of the input."""
        urgency_indicators = [
            "urgent", "asap", "immediately", "now", "quickly", "fast",
            "emergency", "critical", "important", "deadline", "rush"
        ]
        
        urgency_count = sum(1 for indicator in urgency_indicators if indicator in input_lower)
        return min(urgency_count / 5.0, 1.0)
    
    def _calculate_emotional_tone(self, input_lower: str) -> float:
        """Calculate emotional tone (-1.0 to 1.0)."""
        positive_indicators = [
            "good", "great", "excellent", "wonderful", "amazing", "fantastic",
            "love", "like", "enjoy", "happy", "pleased", "satisfied"
        ]
        
        negative_indicators = [
            "bad", "terrible", "awful", "horrible", "hate", "dislike",
            "angry", "frustrated", "annoyed", "upset", "disappointed"
        ]
        
        positive_count = sum(1 for indicator in positive_indicators if indicator in input_lower)
        negative_count = sum(1 for indicator in negative_indicators if indicator in input_lower)
        
        if positive_count + negative_count == 0:
            return 0.0  # Neutral
        
        return (positive_count - negative_count) / (positive_count + negative_count)
    
    def _calculate_confidence(self, input_lower: str) -> float:
        """Calculate confidence level of the input."""
        confidence_indicators = [
            "sure", "certain", "definitely", "absolutely", "confident",
            "know", "understand", "clear", "obvious"
        ]
        
        uncertainty_indicators = [
            "maybe", "perhaps", "might", "could", "possibly", "uncertain",
            "not sure", "don't know", "confused", "unclear"
        ]
        
        confidence_count = sum(1 for indicator in confidence_indicators if indicator in input_lower)
        uncertainty_count = sum(1 for indicator in uncertainty_indicators if indicator in input_lower)
        
        if confidence_count + uncertainty_count == 0:
            return 0.5  # Neutral confidence
        
        return confidence_count / (confidence_count + uncertainty_count)
    
    def select_personality(self, user_input: str) -> PersonalitySelection:
        """Select the most appropriate personality based on user input."""
        # Analyze the input
        pattern = self.analyze_user_input(user_input)
        
        # Calculate personality scores
        personality_scores = self._calculate_personality_scores(pattern)
        
        # Apply user preferences (learned from history)
        personality_scores = self._apply_user_preferences(personality_scores, pattern)
        
        # Select the best personality
        best_personality = max(personality_scores.items(), key=lambda x: x[1])
        selected_profile = best_personality[0]
        confidence_score = best_personality[1]
        
        # Generate reasoning
        reasoning = self._generate_reasoning(pattern, selected_profile, confidence_score)
        
        # Get alternative profiles
        alternative_profiles = sorted(
            [(profile, score) for profile, score in personality_scores.items() if profile != selected_profile],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get selection factors
        selection_factors = self._get_selection_factors(pattern, selected_profile)
        
        selection = PersonalitySelection(
            selected_profile=selected_profile,
            confidence_score=confidence_score,
            reasoning=reasoning,
            alternative_profiles=alternative_profiles,
            selection_factors=selection_factors
        )
        
        # Update user preferences based on this selection
        self._update_user_preferences(pattern, selected_profile)
        
        logger.info(f"Personality selected: {selected_profile.value} (confidence: {confidence_score:.2f})")
        
        return selection
    
    def _calculate_personality_scores(self, pattern: InteractionPattern) -> Dict[PersonalityProfile, float]:
        """Calculate personality scores based on interaction pattern."""
        scores = {profile: 0.0 for profile in PersonalityProfile}
        
        # Base scores from interaction type
        interaction_weights = self.context_weights.get(pattern.interaction_type.value, {})
        for profile, weight in interaction_weights.items():
            scores[profile] += weight * 0.4  # 40% weight for interaction type
        
        # Context-based adjustments
        context_adjustments = self._get_context_adjustments(pattern.data_context)
        for profile, adjustment in context_adjustments.items():
            scores[profile] += adjustment * 0.3  # 30% weight for context
        
        # Complexity-based adjustments
        complexity_adjustments = self._get_complexity_adjustments(pattern.complexity_level)
        for profile, adjustment in complexity_adjustments.items():
            scores[profile] += adjustment * 0.2  # 20% weight for complexity
        
        # Emotional tone adjustments
        emotional_adjustments = self._get_emotional_adjustments(pattern.emotional_tone)
        for profile, adjustment in emotional_adjustments.items():
            scores[profile] += adjustment * 0.1  # 10% weight for emotional tone
        
        # Normalize scores to 0-1 range
        max_score = max(scores.values()) if scores.values() else 1.0
        for profile in scores:
            scores[profile] = scores[profile] / max_score
        
        return scores
    
    def _get_context_adjustments(self, data_context: DataContext) -> Dict[PersonalityProfile, float]:
        """Get context-based adjustments."""
        adjustments = {
            PersonalityProfile.RHO: 0.0,
            PersonalityProfile.LYRA: 0.0,
            PersonalityProfile.NYX: 0.0
        }
        
        if data_context == DataContext.HISTORICAL:
            adjustments[PersonalityProfile.RHO] += 0.3  # Rho excels at historical analysis
        elif data_context == DataContext.CURRENT:
            adjustments[PersonalityProfile.LYRA] += 0.2  # Lyra good at current reflection
        elif data_context == DataContext.FUTURE:
            adjustments[PersonalityProfile.NYX] += 0.3  # Nyx excels at future innovation
        elif data_context == DataContext.TECHNICAL:
            adjustments[PersonalityProfile.RHO] += 0.2  # Rho good at technical analysis
        elif data_context == DataContext.CREATIVE:
            adjustments[PersonalityProfile.NYX] += 0.3  # Nyx excels at creativity
        elif data_context == DataContext.EMOTIONAL:
            adjustments[PersonalityProfile.LYRA] += 0.3  # Lyra excels at emotional understanding
        
        return adjustments
    
    def _get_complexity_adjustments(self, complexity_level: float) -> Dict[PersonalityProfile, float]:
        """Get complexity-based adjustments."""
        adjustments = {
            PersonalityProfile.RHO: 0.0,
            PersonalityProfile.LYRA: 0.0,
            PersonalityProfile.NYX: 0.0
        }
        
        if complexity_level > 0.7:  # High complexity
            adjustments[PersonalityProfile.RHO] += 0.2  # Rho good at complex analysis
        elif complexity_level < 0.3:  # Low complexity
            adjustments[PersonalityProfile.LYRA] += 0.1  # Lyra good at simple collaboration
        else:  # Medium complexity
            adjustments[PersonalityProfile.NYX] += 0.1  # Nyx good at innovative solutions
        
        return adjustments
    
    def _get_emotional_adjustments(self, emotional_tone: float) -> Dict[PersonalityProfile, float]:
        """Get emotional tone-based adjustments."""
        adjustments = {
            PersonalityProfile.RHO: 0.0,
            PersonalityProfile.LYRA: 0.0,
            PersonalityProfile.NYX: 0.0
        }
        
        if emotional_tone > 0.3:  # Positive emotional tone
            adjustments[PersonalityProfile.LYRA] += 0.2  # Lyra good at positive collaboration
        elif emotional_tone < -0.3:  # Negative emotional tone
            adjustments[PersonalityProfile.RHO] += 0.1  # Rho good at analytical problem solving
        else:  # Neutral emotional tone
            adjustments[PersonalityProfile.NYX] += 0.1  # Nyx good at innovative solutions
        
        return adjustments
    
    def _apply_user_preferences(self, scores: Dict[PersonalityProfile, float], pattern: InteractionPattern) -> Dict[PersonalityProfile, float]:
        """Apply learned user preferences."""
        adjusted_scores = scores.copy()
        
        for profile in PersonalityProfile:
            preference_key = f"{profile.value}_{pattern.interaction_type.value}"
            preference = self.user_preferences.get(preference_key, 0.0)
            adjusted_scores[profile] += preference * 0.1  # 10% weight for user preferences
        
        return adjusted_scores
    
    def _generate_reasoning(self, pattern: InteractionPattern, selected_profile: PersonalityProfile, confidence_score: float) -> str:
        """Generate reasoning for personality selection."""
        reasoning_parts = []
        
        # Interaction type reasoning
        interaction_reasoning = {
            PersonalityProfile.RHO: "Rho selected for systematic analysis and preservation focus",
            PersonalityProfile.LYRA: "Lyra selected for collaborative reflection and empathetic understanding",
            PersonalityProfile.NYX: "Nyx selected for innovative solutions and future-oriented thinking"
        }
        reasoning_parts.append(interaction_reasoning[selected_profile])
        
        # Context reasoning
        if pattern.data_context == DataContext.HISTORICAL:
            reasoning_parts.append("Historical context favors analytical approach")
        elif pattern.data_context == DataContext.CREATIVE:
            reasoning_parts.append("Creative context favors innovative approach")
        elif pattern.data_context == DataContext.EMOTIONAL:
            reasoning_parts.append("Emotional context favors empathetic approach")
        
        # Complexity reasoning
        if pattern.complexity_level > 0.7:
            reasoning_parts.append("High complexity requires systematic analysis")
        elif pattern.complexity_level < 0.3:
            reasoning_parts.append("Low complexity allows for collaborative approach")
        
        # Confidence reasoning
        if confidence_score > 0.8:
            reasoning_parts.append("High confidence in selection")
        elif confidence_score < 0.5:
            reasoning_parts.append("Moderate confidence - alternative profiles available")
        
        return " | ".join(reasoning_parts)
    
    def _get_selection_factors(self, pattern: InteractionPattern, selected_profile: PersonalityProfile) -> Dict[str, float]:
        """Get detailed selection factors."""
        return {
            "interaction_type": pattern.interaction_type.value,
            "data_context": pattern.data_context.value,
            "complexity_level": pattern.complexity_level,
            "urgency_level": pattern.urgency_level,
            "emotional_tone": pattern.emotional_tone,
            "confidence_level": pattern.confidence_level,
            "selected_profile": selected_profile.value
        }
    
    def _update_user_preferences(self, pattern: InteractionPattern, selected_profile: PersonalityProfile):
        """Update user preferences based on selection."""
        preference_key = f"{selected_profile.value}_{pattern.interaction_type.value}"
        
        # Simple learning: increase preference for this combination
        self.user_preferences[preference_key] += self.learning_rate
        
        # Decay other preferences slightly
        for key in self.user_preferences:
            if key != preference_key:
                self.user_preferences[key] *= 0.99
    
    def get_selection_history(self) -> List[Dict[str, Any]]:
        """Get history of personality selections."""
        history = []
        for pattern in list(self.interaction_history)[-20:]:  # Last 20 interactions
            history.append({
                "timestamp": pattern.timestamp,
                "interaction_type": pattern.interaction_type.value,
                "data_context": pattern.data_context.value,
                "complexity_level": pattern.complexity_level,
                "emotional_tone": pattern.emotional_tone
            })
        return history
    
    def get_user_preferences(self) -> Dict[str, float]:
        """Get learned user preferences."""
        return dict(self.user_preferences)
    
    def reset_preferences(self):
        """Reset learned user preferences."""
        self.user_preferences.clear()
        logger.info("User preferences reset")

class CollTechAGIIntelligentPersonality:
    """Main class for CollTech-AGI Intelligent Personality Selection."""
    
    def __init__(self):
        self.selector = IntelligentPersonalitySelector()
        self.personality_system = PersonalitySystem()
        self.is_running = False
    
    def start(self):
        """Start the intelligent personality system."""
        self.is_running = True
        print("🧠 COLLTECH-AGI INTELLIGENT PERSONALITY SELECTION")
        print("=" * 70)
        print("Auto-selecting personality based on user interaction patterns")
        print("Learning from user preferences and interaction history")
        print("=" * 70)
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input and auto-select personality."""
        if not self.is_running:
            return {"error": "System not running"}
        
        # Select personality
        selection = self.selector.select_personality(user_input)
        
        # Set the selected personality
        self.personality_system.set_profile(selection.selected_profile)
        
        # Generate response with selected personality
        response = self.personality_system.generate_response(user_input)
        
        return {
            "user_input": user_input,
            "selected_personality": selection.selected_profile.value,
            "confidence_score": selection.confidence_score,
            "reasoning": selection.reasoning,
            "alternative_profiles": [(p.value, score) for p, score in selection.alternative_profiles],
            "selection_factors": selection.selection_factors,
            "personality_response": response
        }
    
    def get_selection_history(self) -> List[Dict[str, Any]]:
        """Get personality selection history."""
        return self.selector.get_selection_history()
    
    def get_user_preferences(self) -> Dict[str, float]:
        """Get learned user preferences."""
        return self.selector.get_user_preferences()
    
    def reset_preferences(self):
        """Reset learned user preferences."""
        self.selector.reset_preferences()
    
    def shutdown(self):
        """Shutdown the system."""
        self.is_running = False
        print("🛑 Intelligent Personality Selection shutdown complete")

def main():
    """Main function to run Intelligent Personality Selection."""
    agi = CollTechAGIIntelligentPersonality()
    agi.start()
    
    print("\n💬 INTELLIGENT PERSONALITY INTERFACE")
    print("=" * 70)
    print("Commands:")
    print("• 'history' - Show selection history")
    print("• 'preferences' - Show learned preferences")
    print("• 'reset' - Reset learned preferences")
    print("• 'quit' or 'exit' - End the session")
    print("=" * 70)
    print("Just type your message and the system will auto-select personality!")
    print("=" * 70)
    
    while agi.is_running:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            elif user_input.lower() == 'history':
                history = agi.get_selection_history()
                print(f"\n📊 Selection History: {len(history)} recent interactions")
                for i, entry in enumerate(history[-5:], 1):  # Show last 5
                    print(f"{i}. {entry['interaction_type']} ({entry['data_context']}) - Complexity: {entry['complexity_level']:.2f}")
            elif user_input.lower() == 'preferences':
                preferences = agi.get_user_preferences()
                print(f"\n🎯 Learned Preferences: {len(preferences)} patterns")
                for pattern, score in list(preferences.items())[:5]:  # Show top 5
                    print(f"• {pattern}: {score:.3f}")
            elif user_input.lower() == 'reset':
                agi.reset_preferences()
                print("\n🔄 User preferences reset")
            else:
                # Process user input with auto-selected personality
                result = agi.process_user_input(user_input)
                print(f"\n🧠 Auto-Selected: {result['selected_personality'].title()} (confidence: {result['confidence_score']:.2f})")
                print(f"💭 Reasoning: {result['reasoning']}")
                print(f"🤖 Response: {result['personality_response']}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    agi.shutdown()
    print("\n🎉 Intelligent Personality Selection session complete!")

if __name__ == "__main__":
    main()
