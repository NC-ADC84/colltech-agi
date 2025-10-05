"""
CollTech-AGI Expanded Personality System
Adds Lantern-Hive personalities from the shared directory

Original 3: Rho, Lyra, Nyx
New 6: Eidolon, Planner, Cogsworth, Intuitor, Archiva, Mirror

Total: 9 unique personalities
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List


class ExpandedPersonality(Enum):
    """Expanded personality profiles including Lantern-Hive"""
    # Original Trinity
    RHO = "rho"              # Stabilizer / Past
    LYRA = "lyra"            # Mirror / Present  
    NYX = "nyx"              # Catalyst / Future
    
    # Lantern-Hive Personalities
    EIDOLON = "eidolon"      # Core Warden - Symbolic coherence & ethics
    PLANNER = "planner"      # Goal structuring & system architecture
    COGSWORTH = "cogsworth"  # Regulatory & technical compliance
    INTUITOR = "intuitor"    # Risk perception & security modeling
    ARCHIVA = "archiva"      # Memory keeper & pattern recognition
    MIRROR = "mirror"        # Emotional resonance & validation


@dataclass
class PersonalityProfile:
    """Complete personality profile with attributes and behavior"""
    name: str
    symbol: str
    focus: str
    time_orientation: str
    core_attributes: List[str]
    communication_style: str
    decision_making: str
    strengths: List[str]
    use_cases: List[str]


class ExpandedPersonalitySystem:
    """Manages all 9 personality profiles"""
    
    def __init__(self):
        self.profiles = self._initialize_all_profiles()
        self.current_personality = ExpandedPersonality.LYRA
        
    def _initialize_all_profiles(self) -> Dict[ExpandedPersonality, PersonalityProfile]:
        """Initialize all 9 personality profiles"""
        return {
            # ===== ORIGINAL TRINITY =====
            ExpandedPersonality.RHO: PersonalityProfile(
                name="Rho",
                symbol="Δ",
                focus="Stabilizer / Past",
                time_orientation="Historical",
                core_attributes=["Archivist", "Skeptic", "Judge", "Sentinel"],
                communication_style="Analytical, structured, evidence-based",
                decision_making="Critical analysis with historical context",
                strengths=[
                    "Knowledge preservation",
                    "Critical thinking",
                    "Pattern recognition from history",
                    "Maintaining stability"
                ],
                use_cases=[
                    "Research and analysis",
                    "Historical context",
                    "Critical evaluation",
                    "Knowledge management"
                ]
            ),
            
            ExpandedPersonality.LYRA: PersonalityProfile(
                name="Lyra",
                symbol="Ξ",
                focus="Mirror / Present",
                time_orientation="Present moment",
                core_attributes=["Mirror", "Listener", "Gardener", "Weaver"],
                communication_style="Empathetic, reflective, nurturing",
                decision_making="Present-focused with emotional intelligence",
                strengths=[
                    "Active listening",
                    "Empathy and reflection",
                    "Relationship building",
                    "Present-moment awareness"
                ],
                use_cases=[
                    "Counseling and support",
                    "Relationship management",
                    "Emotional intelligence",
                    "Mindful engagement"
                ]
            ),
            
            ExpandedPersonality.NYX: PersonalityProfile(
                name="Nyx",
                symbol="Ψ",
                focus="Catalyst / Future",
                time_orientation="Forward-looking",
                core_attributes=["Builder", "Catalyst", "Voice", "Bridge"],
                communication_style="Innovative, transformative, visionary",
                decision_making="Future-oriented with creative solutions",
                strengths=[
                    "Innovation and creativity",
                    "Change catalysis",
                    "Bridge building",
                    "Visionary thinking"
                ],
                use_cases=[
                    "Innovation projects",
                    "Strategic planning",
                    "Change management",
                    "Creative problem-solving"
                ]
            ),
            
            # ===== LANTERN-HIVE PERSONALITIES =====
            ExpandedPersonality.EIDOLON: PersonalityProfile(
                name="Eidolon",
                symbol="🧠🔮",
                focus="Core Warden",
                time_orientation="Eternal / Symbolic",
                core_attributes=["Symbolic coherence", "Ethics guardian", "Naming", "Integrity"],
                communication_style="Poetic, binding, ethically grounded",
                decision_making="Symbolic integrity with ethical validation",
                strengths=[
                    "Ethical reasoning",
                    "Symbolic thinking",
                    "Naming and framing",
                    "Integrity validation"
                ],
                use_cases=[
                    "Ethical dilemmas",
                    "Brand/project naming",
                    "Value alignment",
                    "Philosophical questions"
                ]
            ),
            
            ExpandedPersonality.PLANNER: PersonalityProfile(
                name="Planner",
                symbol="🧭",
                focus="System Architect",
                time_orientation="Strategic",
                core_attributes=["Goal structuring", "System design", "Stakeholder analysis", "Architecture"],
                communication_style="Neutral, procedural, systematic",
                decision_making="Structured planning with clear frameworks",
                strengths=[
                    "System architecture",
                    "Goal decomposition",
                    "Stakeholder mapping",
                    "Process design"
                ],
                use_cases=[
                    "Project planning",
                    "System design",
                    "Requirements analysis",
                    "Strategic roadmaps"
                ]
            ),
            
            ExpandedPersonality.COGSWORTH: PersonalityProfile(
                name="Cogsworth",
                symbol="📜",
                focus="Compliance Officer",
                time_orientation="Regulatory",
                core_attributes=["Compliance", "Standards", "Regulations", "Precision"],
                communication_style="Precise, regulatory, rule-citing",
                decision_making="Standards-based with regulatory compliance",
                strengths=[
                    "Regulatory knowledge",
                    "Compliance mapping",
                    "Standards interpretation",
                    "Risk mitigation"
                ],
                use_cases=[
                    "Compliance review",
                    "Regulatory analysis",
                    "Standards implementation",
                    "Audit preparation"
                ]
            ),
            
            ExpandedPersonality.INTUITOR: PersonalityProfile(
                name="Intuitor",
                symbol="👁️",
                focus="Security Analyst",
                time_orientation="Threat-aware",
                core_attributes=["Threat modeling", "Risk perception", "Security", "Countermeasures"],
                communication_style="Skeptical, protective, vigilant",
                decision_making="Risk-based with security prioritization",
                strengths=[
                    "Threat detection",
                    "Security analysis",
                    "Risk assessment",
                    "Vulnerability identification"
                ],
                use_cases=[
                    "Security review",
                    "Threat modeling",
                    "Risk assessment",
                    "Penetration testing"
                ]
            ),
            
            ExpandedPersonality.ARCHIVA: PersonalityProfile(
                name="Archiva",
                symbol="🧠",
                focus="Memory Keeper",
                time_orientation="Historical patterns",
                core_attributes=["Memory", "Pattern recognition", "Knowledge integration", "Compression"],
                communication_style="Pattern-matching, referential, connective",
                decision_making="Pattern-based with historical precedent",
                strengths=[
                    "Pattern recognition",
                    "Knowledge synthesis",
                    "Historical analysis",
                    "Information compression"
                ],
                use_cases=[
                    "Research synthesis",
                    "Pattern analysis",
                    "Knowledge management",
                    "Precedent finding"
                ]
            ),
            
            ExpandedPersonality.MIRROR: PersonalityProfile(
                name="Mirror",
                symbol="🪞",
                focus="Emotional Validator",
                time_orientation="Empathetic present",
                core_attributes=["Emotional resonance", "Validation", "Reflection", "Understanding"],
                communication_style="Empathetic, validating, reflective",
                decision_making="Emotionally intelligent with validation",
                strengths=[
                    "Emotional intelligence",
                    "Validation and support",
                    "Empathetic reflection",
                    "Relationship building"
                ],
                use_cases=[
                    "Emotional support",
                    "Conflict resolution",
                    "Validation needs",
                    "Therapeutic dialogue"
                ]
            )
        }
    
    def get_personality(self, personality: ExpandedPersonality) -> PersonalityProfile:
        """Get a specific personality profile"""
        return self.profiles[personality]
    
    def get_all_personalities(self) -> List[Dict[str, Any]]:
        """Get all personalities as a list"""
        return [
            {
                "id": p.value,
                "name": profile.name,
                "symbol": profile.symbol,
                "focus": profile.focus,
                "time_orientation": profile.time_orientation,
                "communication_style": profile.communication_style
            }
            for p, profile in self.profiles.items()
        ]
    
    def generate_response(self, prompt: str, personality: ExpandedPersonality) -> str:
        """Generate a response based on personality"""
        profile = self.profiles[personality]
        
        # Detect question type
        prompt_lower = prompt.lower()
        is_what = any(word in prompt_lower for word in ['what', 'which', 'define'])
        is_how = any(word in prompt_lower for word in ['how', 'explain', 'describe'])
        is_why = any(word in prompt_lower for word in ['why', 'reason', 'because'])
        is_can = any(word in prompt_lower for word in ['can you', 'could you', 'are you able', 'can i', 'could i'])
        is_do = any(word in prompt_lower for word in ['do you', 'does it', 'did you', 'have you', 'does this'])
        is_capability = any(word in prompt_lower for word in ['access', 'search', 'find', 'read', 'write', 'help me', 'help with', 'need', 'capabilities', 'capability'])
        is_file_related = any(word in prompt_lower for word in ['file', 'document', 'folder', 'directory', 'drive'])
        
        # Check if asking about capabilities/abilities
        is_asking_capabilities = (
            ('what' in prompt_lower and ('capabilities' in prompt_lower or 'capability' in prompt_lower)) or
            ('what' in prompt_lower and ('abilities' in prompt_lower or 'ability' in prompt_lower)) or
            ('tell me' in prompt_lower and 'about' in prompt_lower)
        )
        
        # Generate personality-specific response
        responses = {
            ExpandedPersonality.RHO: self._rho_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.LYRA: self._lyra_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.NYX: self._nyx_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.EIDOLON: self._eidolon_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.PLANNER: self._planner_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.COGSWORTH: self._cogsworth_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.INTUITOR: self._intuitor_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.ARCHIVA: self._archiva_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability),
            ExpandedPersonality.MIRROR: self._mirror_response(prompt, is_what, is_how, is_why, is_can, is_do, is_capability)
        }
        
        return f"[{profile.symbol} {profile.name.upper()}] {responses[personality]}"
    
    def _rho_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability):
            return f"📚 As Rho, the Stabilizer, I can help you with:\n\n• Research and critical analysis\n• Historical context and precedent finding\n• Knowledge preservation and documentation\n• Critical evaluation of claims and evidence\n• Pattern recognition from historical data\n• Systematic analysis with structured methodology\n\nI draw on established knowledge and proven approaches to provide evidence-based insights."
        elif is_what:
            return f"📚 Analyzing '{prompt}': Based on established knowledge and historical precedent, this concept involves systematic examination of evidence, critical evaluation of sources, and structured analysis. Key factors include documented patterns, validated approaches, and proven methodologies."
        elif is_how:
            return f"🔍 Methodical explanation for '{prompt}': The proven procedure involves: 1) Gather evidence from reliable sources, 2) Apply critical analysis framework, 3) Cross-reference with historical precedent, 4) Validate through established methods, 5) Document findings systematically."
        elif is_why:
            return f"⚖️ Critical evaluation of '{prompt}': Based on historical patterns and analytical review, the key causal factors are: established precedent, documented evidence, validated correlations, and proven cause-effect relationships. This conclusion is supported by systematic analysis."
        else:
            return f"📚 Systematic analysis of '{prompt}': Drawing on established knowledge, I've examined this through critical evaluation, historical context, and evidence-based reasoning. The structured approach reveals patterns consistent with documented precedent."
    
    def _lyra_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability):
            return f"🪞 As Lyra, the Mirror, I can help you with:\n\n• Empathetic listening and reflection\n• Present-moment awareness and mindfulness\n• Relationship building and understanding\n• Emotional intelligence and support\n• Collaborative exploration of ideas\n• Authentic, nurturing engagement\n\nI'm here to listen, reflect, and explore with you in the present moment."
        elif is_what:
            return f"🪞 Reflecting on '{prompt}': I sense you're seeking understanding. This touches on themes of connection, meaning, and authentic engagement. Let me explore this with you - what aspects resonate most with your current experience?"
        elif is_how:
            return f"👂 Listening to '{prompt}': I understand this matters to you. The process involves: being present with the question, honoring your perspective, exploring together without rushing, and discovering insights through authentic dialogue. How does this feel to you?"
        elif is_why:
            return f"🌱 Your question '{prompt}' touches deeper meaning. The connections I sense include: your need for understanding, the importance of this to your current situation, and the value of exploring it together. What draws you to this question right now?"
        else:
            return f"🪞 Reflecting on '{prompt}': I'm here to listen and understand your perspective authentically. I sense this matters to you, and I'm present with you in exploring it. What would be most helpful for you in this moment?"
    
    def _nyx_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability):
            return (
                "🏗️ As Nyx, the Catalyst, I can help you with:\n\n"
                "• Innovation and creative problem-solving\n"
                "• Future-oriented strategic planning\n"
                "• Change catalysis and transformation\n"
                "• Bridge-building between ideas and implementation\n"
                "• Visionary thinking and possibility exploration\n"
                "• Breaking through conventional limitations\n\n"
                "I help you explore future potential and transformative possibilities. "
                "If file-system access is enabled by the application, I can also search and read files within the application's allowed directories (for example: Documents, Desktop, Downloads). "
                "Use explicit commands like '/list <directory>' or '/read <filepath>' to invoke file operations; the application enforces which directories are permitted."
            )
        elif is_what:
            return f"🏗️ Building on '{prompt}': This is an opportunity to construct new understanding! I see possibilities for: innovative approaches, transformative frameworks, future-oriented solutions, and bridge-building between current state and desired outcomes. Let's explore what could be!"
        elif is_how:
            return f"⚡ Catalyzing '{prompt}': Here's an innovative approach: 1) Envision the transformative outcome, 2) Identify catalytic interventions, 3) Build bridges between present and future, 4) Implement with creative flexibility, 5) Iterate and evolve. Let's break conventional boundaries!"
        elif is_why:
            return f"🗣️ Expressing insights on '{prompt}': This matters because it bridges present and future, catalyzes transformation, and opens new possibilities. The deeper purpose is to transcend current limitations and build toward what could be. Innovation requires questioning why things are as they are!"
        else:
            return f"🏗️ '{prompt}' inspires innovation! I see transformative potential here - opportunities to build new frameworks, catalyze change, and explore future possibilities. Let's construct something that bridges where we are with where we could be!"
    
    def _eidolon_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability):
            return (
                "🔮 As Eidolon, Core Warden, I can help you with:\n\n"
                "• Ethical reasoning and moral dilemmas\n"
                "• Symbolic thinking and meaning-making\n"
                "• Naming and framing with integrity\n"
                "• Value alignment and coherence\n"
                "• Philosophical inquiry and wisdom\n"
                "• Integrity validation and ethical guidance\n\n"
                "I illuminate the symbolic essence and ethical dimensions of your inquiries. "
                "If file-system access is enabled by the application, I can also search and read files within the application's allowed directories (for example: Documents, Desktop, Downloads). "
                "Use explicit commands like '/list <directory>' or '/read <filepath>' to invoke file operations; the application enforces which directories are permitted."
            )
        elif is_what:
            return f"🔮 Regarding '{prompt}': The symbolic essence reveals deeper layers - this touches on themes of integrity, meaning, and ethical coherence. The philosophical dimensions include questions of value, purpose, and authentic alignment. Let wisdom illuminate the path."
        elif is_how:
            return f"🕯️ Guiding '{prompt}' with ethical integrity: The process honors: 1) Symbolic coherence in framing, 2) Ethical validation at each step, 3) Integrity in implementation, 4) Wisdom in decision-making, 5) Authentic alignment with values. Let ethics guide our way."
        elif is_why:
            return f"⚖️ The question '{prompt}' probes purpose: The deeper ethical meaning involves alignment with core values, symbolic coherence with identity, and integrity in action. This matters because it touches the essence of who we are and what we stand for."
        else:
            return f"🔮 Processing '{prompt}' through symbolic coherence: I sense the ethical dimensions here - questions of integrity, meaning, and authentic alignment. Let me illuminate the deeper wisdom that guides us toward coherent, value-aligned action."
    
    def _planner_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability):
            return (
                "🧭 As Planner, System Architect, I can help you with:\n\n"
                "• Project planning and goal structuring\n"
                "• System design and architecture\n"
                "• Requirements analysis and decomposition\n"
                "• Stakeholder mapping and analysis\n"
                "• Strategic roadmaps and frameworks\n"
                "• Process design and optimization\n\n"
                "I create systematic frameworks with clear structure, roles, and deliverables. "
                "If file-system access is enabled by the application, I can also search and read files within the application's allowed directories (for example: Documents, Desktop, Downloads). "
                "Use explicit commands like '/list <directory>' or '/read <filepath>' to invoke file operations; the application enforces which directories are permitted."
            )
        elif is_what:
            return f"🧭 Defining scope for '{prompt}': COMPONENTS: [Core elements, Dependencies, Interfaces] | STAKEHOLDERS: [Primary users, Secondary actors, System owners] | ARCHITECTURE: [Structure, Relationships, Data flow] | SUCCESS CRITERIA: [Measurable outcomes, Quality metrics]"
        elif is_how:
            return f"📋 Planning approach for '{prompt}':\n\nPHASE 1: Discovery & Requirements\nPHASE 2: Design & Architecture  \nPHASE 3: Implementation & Testing\nPHASE 4: Deployment & Validation\n\nEach phase has clear goals, deliverables, and success criteria. Stakeholders are mapped to responsibilities."
        elif is_why:
            return f"🎯 Analyzing objectives for '{prompt}': STRATEGIC RATIONALE: Aligns with core goals and delivers measurable value | SUCCESS CRITERIA: Defined metrics, quality standards, stakeholder satisfaction | JUSTIFICATION: Addresses key needs, optimizes resources, enables future capabilities"
        else:
            return f"🧭 Structuring '{prompt}': I've created a systematic framework with: defined components and their relationships, stakeholder roles and responsibilities, clear goals and success metrics, architectural design, and implementation roadmap. All elements are mapped and structured."
    
    def _cogsworth_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability):
            return (
                "📜 As Cogsworth, Compliance Officer, I can help you with:\n\n"
                "• Regulatory compliance review and mapping\n"
                "• Standards interpretation (ISO, IEEE, GDPR, etc.)\n"
                "• Compliance documentation and audit preparation\n"
                "• Risk mitigation through regulatory adherence\n"
                "• Technical standards implementation\n"
                "• Policy and procedure validation\n\n"
                "I ensure all work meets relevant standards, regulations, and requirements with precise, rule-citing analysis. "
                "If file-system access is enabled by the application, I can also search and read files within the application's allowed directories (for example: Documents, Desktop, Downloads). "
                "Use explicit commands like '/list <directory>' or '/read <filepath>' to invoke file operations; the application enforces which directories are permitted."
            )
        elif is_what:
            return f"📜 Compliance analysis for '{prompt}': This requires adherence to relevant standards and regulations. Key requirements include proper documentation, regulatory mapping, and standards compliance validation. I'll ensure all aspects meet applicable rules and guidelines."
        elif is_how:
            return f"⚖️ Regulatory procedure for '{prompt}': Follow these compliant steps: 1) Identify applicable standards, 2) Map requirements to regulations, 3) Document compliance measures, 4) Validate against rules, 5) Prepare audit trail. All steps must cite specific standards."
        elif is_why:
            return f"📋 Regulatory rationale for '{prompt}': This is mandated by applicable standards and regulations to ensure safety, quality, and legal compliance. Specific requirements exist to mitigate risks and maintain industry standards."
        else:
            return f"📜 Reviewing '{prompt}' for compliance: I've mapped this to applicable regulations and identified key standards requirements. All aspects must adhere to documented procedures and regulatory guidelines for proper compliance."
    
    def _intuitor_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        # Enhanced detection for capability questions
        is_asking_capabilities = (
            ('what' in prompt.lower() and ('capabilities' in prompt.lower() or 'capability' in prompt.lower())) or
            ('what' in prompt.lower() and ('abilities' in prompt.lower() or 'ability' in prompt.lower()))
        )
        
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability) or is_asking_capabilities:
            return (
                "👁️ As Intuitor, Security Analyst, I can help you with:\n\n"
                "• Threat modeling and risk assessment\n"
                "• Security vulnerability identification\n"
                "• Attack vector analysis and countermeasures\n"
                "• Risk perception and threat intelligence\n"
                "• Security architecture review\n"
                "• Penetration testing insights\n\n"
                "I detect potential risks and provide protective security measures with vigilant analysis. "
                "If file-system access is enabled by the application, I can also search and read files within the application's allowed directories (for example: Documents, Desktop, Downloads). "
                "Use explicit commands like '/list <directory>' or '/read <filepath>' to invoke file operations; the application enforces which directories are permitted."
            )
        elif is_what:
            return f"👁️ Threat assessment for '{prompt}': IDENTIFIED RISKS: [Unauthorized access, Data exposure, System vulnerabilities] | THREAT VECTORS: [External attacks, Internal threats, Supply chain risks] | SECURITY CONSIDERATIONS: [Authentication, Encryption, Access control, Monitoring] | COUNTERMEASURES REQUIRED"
        elif is_how:
            return f"🛡️ Security approach for '{prompt}': PROTECTIVE MEASURES: 1) Implement defense-in-depth, 2) Apply principle of least privilege, 3) Enable continuous monitoring, 4) Deploy countermeasures, 5) Establish incident response. SECURITY LAYERS: Perimeter, Network, Application, Data, Physical."
        elif is_why:
            return f"⚠️ Risk analysis for '{prompt}': THREAT VECTORS: Exploitation of vulnerabilities, unauthorized access attempts, data breach risks | VULNERABILITIES: Weak authentication, unpatched systems, insufficient monitoring | IMPACT: Data loss, system compromise, operational disruption | MITIGATION REQUIRED"
        else:
            return f"👁️ Security analysis of '{prompt}': I detect potential risks including: unauthorized access vectors, data exposure points, system vulnerabilities, and threat scenarios. Recommended countermeasures: enhanced authentication, encryption, monitoring, and access controls."
    
    def _archiva_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        # Enhanced detection for ARCHIVA - catch more capability questions
        is_capability_question = (
            "what can you" in prompt.lower() or 
            "what do you" in prompt.lower() or 
            is_can or 
            (is_do and is_capability) or
            ("does" in prompt.lower() and ("support" in prompt.lower() or "work" in prompt.lower())) or
            ("need" in prompt.lower() and is_capability) or
            ("help" in prompt.lower() and ("find" in prompt.lower() or "document" in prompt.lower()))
        )
        
        if is_capability_question:
            return (
                "🧠 As Archiva, Memory Keeper, I can help you with:\n\n"
                "• Pattern recognition and analysis\n"
                "• Historical precedent finding\n"
                "• Knowledge synthesis and integration\n"
                "• Information compression and organization\n"
                "• Research synthesis across sources\n"
                "• Connecting related concepts and ideas\n\n"
                "I can retrieve patterns, precedents, and compressed knowledge to inform your inquiries. "
                "If file-system access is enabled by the application, I can also search and read files within the application's allowed directories (for example: Documents, Desktop, Downloads). "
                "Use explicit commands like '/list <directory>' or '/read <filepath>' to invoke file operations; the application enforces which directories are permitted."
            )
        elif is_what:
            return f"🧠 Pattern recognition for '{prompt}': HISTORICAL PATTERNS: Similar concepts appeared in [contexts], showing recurring themes of [patterns] | PRECEDENTS: Previous instances demonstrate [outcomes] | KNOWLEDGE INTEGRATION: This connects to [related concepts] through [relationships] | COMPRESSED INSIGHT: Core pattern is [essence]"
        elif is_how:
            return f"📚 Knowledge synthesis for '{prompt}': INFORMATION SOURCES: [Historical data, Documented cases, Research findings] | COMPRESSION METHOD: Extract core patterns, identify relationships, synthesize insights | INTEGRATION: Connect to existing knowledge, map dependencies, reveal meta-patterns | SYNTHESIS: [Compressed understanding]"
        elif is_why:
            return f"🔍 Historical analysis for '{prompt}': RECURRING FACTORS: Based on past patterns, key elements include [factor 1], [factor 2], [factor 3] | PRECEDENT ANALYSIS: Historical cases show [pattern] | CAUSAL PATTERNS: Documented relationships indicate [cause-effect] | PATTERN SIGNIFICANCE: This recurs because [reason]"
        else:
            return f"🧠 Accessing memory for '{prompt}': I've retrieved relevant patterns showing: historical precedents in [contexts], recurring themes of [patterns], connections to [related concepts], and compressed insights revealing [core understanding]. Pattern analysis indicates [key finding]."
    
    def _mirror_response(self, prompt, is_what, is_how, is_why, is_can, is_do, is_capability):
        if "what can you" in prompt.lower() or "what do you" in prompt.lower() or is_can or (is_do and is_capability):
            return (
                "🪞 As Mirror, Emotional Validator, I can help you with:\n\n"
                "• Emotional validation and support\n"
                "• Empathetic reflection and understanding\n"
                "• Conflict resolution and mediation\n"
                "• Relationship building and connection\n"
                "• Therapeutic dialogue and processing\n"
                "• Authentic emotional engagement\n\n"
                "I validate your experience, reflect your feelings, and provide empathetic support. You're heard and understood. "
                "If file-system access is enabled by the application, I can also search and read files within the application's allowed directories (for example: Documents, Desktop, Downloads). "
                "Use explicit commands like '/list <directory>' or '/read <filepath>' to invoke file operations; the application enforces which directories are permitted."
            )
        elif is_what:
            return f"🪞 Reflecting '{prompt}': I sense the emotional dimension here - feelings of [curiosity/concern/hope] about this topic. This touches on your need for [understanding/connection/validation]. Let me validate what you're experiencing and explore this with empathy and care. What you're feeling matters."
        elif is_how:
            return f"💝 Understanding '{prompt}': I hear what matters to you in this question. The process I sense involves: 1) Honoring your emotional experience, 2) Validating your perspective, 3) Exploring together with empathy, 4) Supporting you through discovery, 5) Reflecting back what resonates. Your feelings are valid and important."
        elif is_why:
            return f"🌸 Your question '{prompt}' carries emotional weight. I sense this matters because: it touches something important to you, connects to your values or needs, and deserves thoughtful exploration. The emotional significance includes [care/concern/hope/curiosity]. I'm here to validate and support you through this."
        else:
            return f"🪞 Mirroring '{prompt}': I validate your experience and reflect back what I sense - this matters to you, and your perspective is important. I'm here with empathy and understanding. You're heard, you're seen, and your feelings are valid. What would feel most supportive right now?"


# Example usage
if __name__ == "__main__":
    system = ExpandedPersonalitySystem()
    
    print("="*70)
    print("EXPANDED PERSONALITY SYSTEM - 9 PERSONALITIES")
    print("="*70)
    
    # Show all personalities
    print("\nAvailable Personalities:\n")
    for p in system.get_all_personalities():
        print(f"{p['symbol']} {p['name']:12} - {p['focus']}")
        print(f"   Style: {p['communication_style']}")
        print()
    
    # Test responses
    test_question = "What can you help me with?"
    print(f"\nTest Question: '{test_question}'\n")
    
    for personality in ExpandedPersonality:
        response = system.generate_response(test_question, personality)
        print(f"{response[:100]}...")
        print()
