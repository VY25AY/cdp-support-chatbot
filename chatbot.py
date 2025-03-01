import os
import re
from typing import Dict, Optional, List, Tuple

class CDPChatbot:
    def __init__(self):
        self.docs: Dict[str, str] = {}
        self.cdp_names = ['segment', 'mparticle', 'lytics', 'zeotap']
        self._load_documentation()

    def _load_documentation(self):
        """Load documentation files for each CDP."""
        docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
        for cdp in self.cdp_names:
            try:
                with open(os.path.join(docs_dir, f'{cdp}.txt'), 'r') as f:
                    self.docs[cdp] = f.read()
            except FileNotFoundError:
                print(f"Warning: Documentation file for {cdp} not found")

    def _identify_cdp(self, question: str) -> List[str]:
        """Identify which CDP(s) the question is about."""
        mentioned_cdps = []
        for cdp in self.cdp_names:
            if cdp.lower() in question.lower():
                mentioned_cdps.append(cdp)
        return mentioned_cdps

    def _is_comparison_question(self, question: str) -> bool:
        """Check if the question is asking for a comparison between CDPs."""
        comparison_keywords = ['compare', 'comparison', 'versus', 'vs', 'difference', 'different']
        return any(keyword in question.lower() for keyword in comparison_keywords)

    def _extract_relevant_info(self, cdp: str, question: str) -> str:
        """Extract relevant information from the documentation based on the question."""
        if cdp not in self.docs:
            return f"I apologize, but I don't have access to {cdp}'s documentation at the moment."

        # Split documentation into sections
        sections = self.docs[cdp].split('\n\n')
        
        # Extract keywords from question (excluding common words)
        stop_words = {'how', 'can', 'the', 'and', 'for', 'to', 'in', 'i', 'a', 'do', 'does', 'compare'}
        keywords = [word.lower() for word in question.split() 
                   if len(word) > 2 and word.lower() not in stop_words]
        
        # Add related terms for better matching
        keyword_mapping = {
            'audience': {'segment', 'segments', 'segmentation', 'personas'},
            'create': {'build', 'making', 'setup', 'configure'},
            'profile': {'identity', 'user', 'customer'},
            'source': {'input', 'integration', 'connector'}
        }
        
        expanded_keywords = set(keywords)
        for keyword in keywords:
            for key, related_terms in keyword_mapping.items():
                if keyword in related_terms or keyword == key:
                    expanded_keywords.update(related_terms)
        
        # Score sections based on:
        # 1. Title match (higher weight)
        # 2. Keyword matches in content
        # 3. Section position (earlier sections slightly preferred)
        scored_sections = []
        for i, section in enumerate(sections):
            lines = section.split('\n')
            if not lines:  # Skip empty sections
                continue
                
            title = lines[0].lower()
            content = ' '.join(lines[1:]).lower()
            
            # Calculate scores with expanded keywords
            title_score = sum(3 for keyword in expanded_keywords if keyword in title)
            content_score = sum(1 for keyword in expanded_keywords if keyword in content)
            position_score = 1.0 / (i + 1)  # Earlier sections get slightly higher scores
            
            total_score = title_score + content_score + position_score
            
            if total_score > 0:
                scored_sections.append((total_score, section))
        
        # Return most relevant section(s)
        if scored_sections:
            scored_sections.sort(reverse=True)
            best_section = scored_sections[0][1]
            
            # Format the response
            lines = best_section.split('\n')
            if len(lines) > 1:
                steps = '\n'.join(lines[1:])
                return f"{steps}"
        
        return f"I couldn't find specific information about that in {cdp}'s documentation. Could you try rephrasing your question?"

    def _handle_comparison(self, cdps: List[str], question: str) -> str:
        """Handle questions comparing multiple CDPs."""
        if len(cdps) < 2:
            return "To compare CDPs, please mention at least two platforms in your question."
        
        # Get relevant information for each CDP
        responses = {}
        for cdp in cdps:
            info = self._extract_relevant_info(cdp, question)
            if not info.startswith("I couldn't find"):
                responses[cdp] = info

        if not responses:
            return "I couldn't find relevant comparison information. Please try rephrasing your question."

        # Format the comparison response
        comparison = []
        for cdp, info in responses.items():
            comparison.append(f"{cdp.capitalize()}:\n{info}")

        return "\n\nComparison:\n\n" + "\n\n".join(comparison)

    def _is_irrelevant_question(self, question: str) -> bool:
        """Check if the question is irrelevant to CDPs."""
        cdp_related_keywords = ['cdp', 'platform', 'data', 'segment', 'mparticle', 'lytics', 'zeotap',
                              'source', 'integration', 'profile', 'audience', 'analytics']
        return not any(keyword in question.lower() for keyword in cdp_related_keywords)

    def answer_question(self, question: str) -> str:
        """Process and answer a user's question."""
        # Check if question is irrelevant to CDPs
        if self._is_irrelevant_question(question):
            return ("I'm a CDP support chatbot. I can help you with questions about Segment, mParticle, "
                   "Lytics, and Zeotap. Please ask me something related to these platforms.")

        # Identify mentioned CDPs
        mentioned_cdps = self._identify_cdp(question)

        # If no specific CDP is mentioned, try to infer from context
        if not mentioned_cdps:
            # Look for task-specific keywords to infer the CDP
            if 'source' in question.lower():
                mentioned_cdps = ['segment']  # Segment is known for source management
            elif 'profile' in question.lower():
                mentioned_cdps = ['mparticle']  # mParticle is known for profile management
            else:
                return ("Could you please specify which CDP you're asking about? "
                       "(Segment, mParticle, Lytics, or Zeotap)")

        # Handle comparison questions
        if self._is_comparison_question(question):
            return self._handle_comparison(mentioned_cdps, question)

        # Handle single CDP questions
        return self._extract_relevant_info(mentioned_cdps[0], question)

# Global chatbot instance
chatbot = None

def answer_howto_question(question: str) -> str:
    """Interface function to get answers from the chatbot."""
    try:
        global chatbot
        if chatbot is None:
            print("Initializing new chatbot instance...")
            chatbot = CDPChatbot()
        
        print(f"Processing question: {question}")
        response = chatbot.answer_question(question)
        print(f"Generated response: {response}")
        return response
    except Exception as e:
        print(f"Error in answer_howto_question: {str(e)}")
        return f"I apologize, but I encountered an error: {str(e)}"
