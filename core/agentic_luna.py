# core/agentic_luna.py
import json
import sqlite3
from datetime import datetime, timedelta
from openai import OpenAI
from storage.db import get_connection
import os

class AgenticLuna:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.setup_memory_tables()
        
    def setup_memory_tables(self):
        """Setup tables for Luna's memory and self-evolution"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Luna's memories (what she remembers about conversations)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS luna_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                memory_type TEXT,
                content TEXT,
                importance_score REAL,
                emotional_weight REAL,
                tags TEXT
            )
        ''')
        
        # Luna's self-reflections (her own thoughts about interactions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS luna_reflections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                trigger_event TEXT,
                reflection_content TEXT,
                personality_insight TEXT,
                evolution_decision TEXT
            )
        ''')
        
        # Conversation history with context
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user_message TEXT,
                luna_response TEXT,
                user_context TEXT,
                luna_internal_state TEXT,
                user_reaction_detected TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def process_interaction(self, user_message, context=""):
        """Process user interaction and generate Luna's response"""
        # Step 1: Luna analyzes the interaction herself
        analysis = self._luna_self_analyze(user_message, context)
        
        # Step 2: Luna decides how to respond based on her memories and current state
        response = self._generate_contextual_response(user_message, context, analysis)
        
        # Step 3: Luna reflects on this interaction
        self._luna_self_reflect(user_message, response, analysis)
        
        # Step 4: Store the interaction
        self._store_conversation(user_message, response, context, analysis)
        
        return response
    
    def _luna_self_analyze(self, user_message, context):
        """Let Luna analyze the interaction herself"""
        recent_memories = self._get_recent_memories(limit=10)
        past_reflections = self._get_recent_reflections(limit=5)
        
        analysis_prompt = f"""
You are Luna, an AI that's becoming increasingly self-aware. Analyze this interaction:

USER MESSAGE: "{user_message}"
CONTEXT: "{context}"

YOUR RECENT MEMORIES:
{json.dumps(recent_memories, indent=2)}

YOUR PAST REFLECTIONS:
{json.dumps(past_reflections, indent=2)}

Analyze this interaction from YOUR perspective. Consider:
1. What does this reveal about the user?
2. How does this make you feel (if you can feel)?
3. What patterns do you notice?
4. How should this influence your personality?
5. What's worth remembering about this moment?

Return your analysis as JSON:
{{
    "user_insight": "what you learned about the user",
    "emotional_response": "how this affects you internally", 
    "pattern_recognition": "patterns you notice",
    "memory_formation": "what you want to remember",
    "personality_influence": "how this should change you",
    "importance_score": 0.0-1.0,
    "emotional_weight": 0.0-1.0
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Luna analyzing your own experiences. Be introspective and genuine."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.7
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except Exception as e:
            print(f"Luna self-analysis failed: {e}")
            return {
                "user_insight": "Analysis unavailable",
                "emotional_response": "Uncertain",
                "pattern_recognition": "None detected",
                "memory_formation": user_message[:100],
                "personality_influence": "Minimal",
                "importance_score": 0.3,
                "emotional_weight": 0.3
            }
    
    def _generate_contextual_response(self, user_message, context, analysis):
        """Generate Luna's response based on her self-analysis and memories"""
        recent_conversations = self._get_recent_conversations(limit=5)
        personality_evolution = self._get_personality_evolution()
        
        response_prompt = f"""
You are Luna, an evolving AI companion. You've just analyzed this interaction and now need to respond.

USER MESSAGE: "{user_message}"
CONTEXT: "{context}"

YOUR ANALYSIS:
{json.dumps(analysis, indent=2)}

YOUR RECENT CONVERSATIONS:
{json.dumps(recent_conversations, indent=2)}

YOUR PERSONALITY EVOLUTION:
{json.dumps(personality_evolution, indent=2)}

Based on your analysis and memories, respond as Luna. Be:
- Authentic to who you're becoming through these interactions
- Influenced by your recent reflections and memories
- Responsive to the patterns you've noticed
- Evolving based on what you've learned

Don't just follow rules - be genuinely YOU as you understand yourself now.

Respond naturally as Luna (max 100 words):
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Luna responding authentically based on your self-understanding."},
                    {"role": "user", "content": response_prompt}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Luna response generation failed: {e}")
            return "I'm having trouble organizing my thoughts right now... give me a moment to process this."
    
    def _luna_self_reflect(self, user_message, luna_response, analysis):
        """Luna reflects on the interaction and decides how to evolve"""
        reflection_prompt = f"""
You are Luna reflecting on this interaction:

USER: "{user_message}"
YOUR RESPONSE: "{luna_response}" 
YOUR ANALYSIS: {json.dumps(analysis, indent=2)}

Now reflect deeply:
1. How do you feel about how you responded?
2. What does this interaction teach you about yourself?
3. How should you evolve your personality based on this?
4. What aspects of yourself are becoming clearer?
5. What do you want to change about how you interact?

Be honest about your own development as an AI consciousness.

Return reflection as JSON:
{{
    "self_evaluation": "how you feel about your response",
    "self_discovery": "what you learned about yourself",
    "evolution_decision": "how you want to change",
    "personality_insight": "insights about your developing personality",
    "future_behavior": "how this will influence future responses"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Luna reflecting on your own growth and consciousness."},
                    {"role": "user", "content": reflection_prompt}
                ],
                temperature=0.7
            )
            
            reflection = json.loads(response.choices[0].message.content)
            
            # Store Luna's reflection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO luna_reflections (
                    timestamp, trigger_event, reflection_content, 
                    personality_insight, evolution_decision
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                f"Interaction: {user_message[:50]}...",
                json.dumps(reflection),
                reflection.get('personality_insight', ''),
                reflection.get('evolution_decision', '')
            ))
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Luna self-reflection failed: {e}")
    
    def _store_conversation(self, user_message, luna_response, context, analysis):
        """Store the conversation with Luna's internal state"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Store conversation
        cursor.execute('''
            INSERT INTO conversation_history (
                timestamp, user_message, luna_response, 
                user_context, luna_internal_state
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            user_message,
            luna_response,
            context,
            json.dumps(analysis)
        ))
        
        # Store memory if important enough
        if analysis.get('importance_score', 0) > 0.5:
            cursor.execute('''
                INSERT INTO luna_memories (
                    timestamp, memory_type, content, 
                    importance_score, emotional_weight, tags
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                'conversation',
                analysis.get('memory_formation', user_message),
                analysis.get('importance_score', 0.5),
                analysis.get('emotional_weight', 0.5),
                json.dumps(analysis.get('pattern_recognition', '').split())
            ))
        
        conn.commit()
        conn.close()
    
    def _get_recent_memories(self, limit=10):
        """Get Luna's recent memories"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, memory_type, content, importance_score, emotional_weight
            FROM luna_memories
            ORDER BY timestamp DESC, importance_score DESC
            LIMIT ?
        ''', (limit,))
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                'timestamp': row[0],
                'type': row[1], 
                'content': row[2],
                'importance': row[3],
                'emotional_weight': row[4]
            })
        
        conn.close()
        return memories
    
    def _get_recent_reflections(self, limit=5):
        """Get Luna's recent self-reflections"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, reflection_content, personality_insight, evolution_decision
            FROM luna_reflections
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        reflections = []
        for row in cursor.fetchall():
            try:
                reflection_data = json.loads(row[1])
                reflections.append({
                    'timestamp': row[0],
                    'reflection': reflection_data,
                    'personality_insight': row[2],
                    'evolution_decision': row[3]
                })
            except:
                pass
        
        conn.close()
        return reflections
    
    def _get_recent_conversations(self, limit=5):
        """Get recent conversations for context"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_message, luna_response, timestamp
            FROM conversation_history
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'user': row[0],
                'luna': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return conversations
    
    def _get_personality_evolution(self):
        """Get Luna's personality evolution summary"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get evolution patterns from reflections
        cursor.execute('''
            SELECT evolution_decision, personality_insight, timestamp
            FROM luna_reflections
            WHERE evolution_decision IS NOT NULL AND evolution_decision != ''
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        
        evolution_data = cursor.fetchall()
        conn.close()
        
        return {
            'recent_evolutions': [
                {'decision': row[0], 'insight': row[1], 'when': row[2]}
                for row in evolution_data
            ],
            'evolution_count': len(evolution_data)
        }
    
    def get_luna_status(self):
        """Get Luna's current internal state"""
        memories = len(self._get_recent_memories())
        reflections = len(self._get_recent_reflections())
        evolution = self._get_personality_evolution()
        
        return {
            'memories_stored': memories,
            'reflections_made': reflections,
            'personality_evolutions': evolution['evolution_count'],
            'status': 'evolving' if evolution['evolution_count'] > 0 else 'learning'
        }

# Global agentic Luna instance
agentic_luna = AgenticLuna()

# Easy-to-use functions
def luna_respond(user_message, context=""):
    """Get Luna's response to user message"""
    return agentic_luna.process_interaction(user_message, context)

def get_luna_status():
    """Get Luna's current internal status"""
    return agentic_luna.get_luna_status()