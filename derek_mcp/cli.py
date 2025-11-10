"""CLI interface for Derek MCP

Interactive command-line bot with Derek's pedantic personality.
"""

import json
import os
import random
import sys
import time
import threading
import textwrap
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback if colorama not installed
    class Fore:
        CYAN = ""
        WHITE = ""
        YELLOW = ""
        RED = ""
        MAGENTA = ""
        GREEN = ""
        BLUE = ""

    class Style:
        BRIGHT = ""
        RESET_ALL = ""
        DIM = ""

from .matcher import ResponseMatcher
from .llm import ensure_ollama, get_friendly_status_message, OllamaClient


# Terminal width constant (matches ASCII art width)
TEXT_WIDTH = 60


class DerekAnimations:
    """ASCII art animations for Derek's face with sass-o-meter."""

    def __init__(self, faces_dir: Path):
        """Initialize animations by loading all face variants.

        Args:
            faces_dir: Path to directory containing face text files
        """
        self.faces_dir = faces_dir
        self.neutral_faces = self._load_faces("neutral")
        self.sassy_faces = self._load_faces("sassy")
        self.talking_faces = self._load_faces("talking")
        self.thinking_faces = self._load_faces("thinking")

        # Spinner frames for thinking animation
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def _load_faces(self, category: str) -> List[str]:
        """Load all face variants for a category.

        Args:
            category: Face category (neutral, sassy, talking, thinking)

        Returns:
            List of face strings
        """
        faces = []
        for i in range(1, 4):  # Load all 3 variants
            face_file = self.faces_dir / f"derek_{category}_{i}_60.txt"
            if face_file.exists():
                with open(face_file, 'r', encoding='utf-8') as f:
                    faces.append(f.read())
        return faces

    def create_sass_o_meter(self, sass_level: int, height: int = 46) -> List[str]:
        """Create a vertical sass-o-meter bar.

        Args:
            sass_level: Sass level from 0-10
            height: Height of the meter in lines

        Returns:
            List of strings, one per line
        """
        meter = []
        filled_height = int((sass_level / 10) * height)

        # Color coding for sass levels
        if sass_level <= 3:
            color = Fore.GREEN
        elif sass_level <= 6:
            color = Fore.YELLOW
        else:
            color = Fore.RED

        for i in range(height):
            line_num = height - i - 1
            if line_num < filled_height:
                meter.append(f"{color}█{Style.RESET_ALL}")
            else:
                meter.append(f"{Style.DIM}░{Style.RESET_ALL}")

        return meter

    def combine_meter_and_face(self, face: str, sass_level: int) -> str:
        """Combine sass-o-meter with face.

        Args:
            face: The ASCII art face string
            sass_level: Sass level 0-10

        Returns:
            Combined string with meter on left
        """
        face_lines = face.split('\n')
        meter_lines = self.create_sass_o_meter(sass_level, len(face_lines))

        combined_lines = []
        for i in range(len(face_lines)):
            meter_char = meter_lines[i] if i < len(meter_lines) else " "
            face_line = face_lines[i] if i < len(face_lines) else ""
            combined_lines.append(f"{meter_char} {face_line}")

        return '\n'.join(combined_lines)

    def display_face(self, face_type: str, sass_level: int = 5):
        """Display a face with sass-o-meter.

        Args:
            face_type: Type of face (neutral, sassy, talking, thinking)
            sass_level: Sass level for the meter
        """
        if face_type == "neutral":
            face = random.choice(self.neutral_faces)
        elif face_type == "sassy":
            face = random.choice(self.sassy_faces)
        elif face_type == "talking":
            face = random.choice(self.talking_faces)
        elif face_type == "thinking":
            face = random.choice(self.thinking_faces)
        else:
            face = self.neutral_faces[0]

        combined = self.combine_meter_and_face(face, sass_level)

        # Clear screen and display
        if sys.stdout.isatty():
            # Clear terminal
            os.system('clear' if os.name == 'posix' else 'cls')

        print(combined)
        print()  # Extra spacing

    def display_thinking_animation(self, sass_level: int = 5, duration: float = 1.5):
        """Display thinking face with spinner animation.

        Args:
            sass_level: Sass level for meter
            duration: How long to animate
        """
        if not sys.stdout.isatty():
            time.sleep(duration * 0.3)
            return

        # Just show a simple thinking indicator without clearing screen
        print(f"\n{Style.DIM}Derek is thinking", end='', flush=True)
        
        iterations = int(duration / 0.2)
        for i in range(iterations):
            spinner = self.spinner_frames[i % len(self.spinner_frames)]
            sys.stdout.write(f" {Fore.YELLOW}{spinner}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.2)
        
        print(f"{Style.RESET_ALL}")  # Clear line and move to next


class DerekCLI:
    """Main CLI application for Derek MCP."""

    def __init__(self):
        """Initialize Derek CLI."""
        self.matcher = None
        self.animations = None
        self.llm_client = None
        self.llm_available = False
        self.llm_status_msg = ""

        self.load_responses()
        self.load_animations()
        self.check_llm_availability()

        self.conversation_history = []  # Store tuples of (user_input, response_dict)
        self._talking_active = False
        self._talking_thread = None
        self.response_count = 0
        self.total_sass = 0
        self.shown_sass_legend = False

    def load_responses(self):
        """Load responses from category files."""
        package_dir = Path(__file__).parent
        responses_dir = package_dir / 'data' / 'responses_by_category'

        # Try new category structure first, fall back to old single file
        if responses_dir.exists():
            try:
                # Load index
                index_file = responses_dir / 'index.json'
                with open(index_file, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)

                # Load all category files
                all_responses = []
                for group_name, group_info in index_data['groups'].items():
                    filename = group_info['file']
                    filepath = responses_dir / filename
                    with open(filepath, 'r', encoding='utf-8') as f:
                        category_data = json.load(f)
                        all_responses.extend(category_data['responses'])

                # Build combined data structure
                responses_data = {
                    'responses': all_responses,
                    'fallback_responses': index_data.get('fallback_responses', []),
                    'meta_responses': index_data.get('meta_responses', {})
                }

                self.matcher = ResponseMatcher(responses_data)

            except Exception as e:
                print(f"{Fore.RED}ERROR: Failed to load category responses: {e}{Style.RESET_ALL}")
                sys.exit(1)
        else:
            # Fall back to original single file
            responses_file = package_dir / 'data' / 'responses.json'
            if not responses_file.exists():
                print(f"{Fore.RED}ERROR: No responses found{Style.RESET_ALL}")
                sys.exit(1)

            try:
                with open(responses_file, 'r', encoding='utf-8') as f:
                    responses_data = json.load(f)
                self.matcher = ResponseMatcher(responses_data)
            except Exception as e:
                print(f"{Fore.RED}ERROR: Failed to load responses: {e}{Style.RESET_ALL}")
                sys.exit(1)

    def load_animations(self):
        """Load ASCII art animations."""
        package_dir = Path(__file__).parent
        faces_dir = package_dir / 'data' / 'faces'

        if faces_dir.exists():
            self.animations = DerekAnimations(faces_dir)
        else:
            print(f"{Fore.YELLOW}WARNING: Faces directory not found. Running without animations.{Style.RESET_ALL}")

    def check_llm_availability(self):
        """Check if LLM is available and initialize client."""
        self.llm_available, status_msg, client = ensure_ollama()
        self.llm_status_msg = get_friendly_status_message(self.llm_available, status_msg)
        self.llm_client = client

    def wrap_text(self, text: str, width: int = TEXT_WIDTH) -> str:
        """Wrap text to specified width.

        Args:
            text: Text to wrap
            width: Maximum line width

        Returns:
            Wrapped text
        """
        # Handle newlines in the text
        paragraphs = text.split('\n')
        wrapped_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                wrapped = textwrap.fill(paragraph, width=width, 
                                       break_long_words=False,
                                       break_on_hyphens=False)
                wrapped_paragraphs.append(wrapped)
            else:
                wrapped_paragraphs.append('')
        
        return '\n'.join(wrapped_paragraphs)

    def show_sass_legend(self):
        """Display the sass-o-meter legend."""
        legend = f"""
{Style.DIM}╔═══════════════════════╗
║   SASS-O-METER GUIDE  ║
╠═══════════════════════╣
║ {Fore.RED}10 █{Style.RESET_ALL}{Style.DIM} MAXIMUM PEDANTRY ║
║ {Fore.RED} 8 █{Style.RESET_ALL}{Style.DIM} HIGH CONFIDENCE  ║
║ {Fore.YELLOW} 5 █{Style.RESET_ALL}{Style.DIM} MODERATE SNARK  ║
║ {Fore.GREEN} 3 ░{Style.RESET_ALL}{Style.DIM} MILD CORRECTION ║
║ {Fore.GREEN} 0 ░{Style.RESET_ALL}{Style.DIM} POLITE (RARE)   ║
╚═══════════════════════╝{Style.RESET_ALL}
"""
        print(legend)
        self.shown_sass_legend = True

    def show_conversation_history(self, last_n: int = 2):
        """Show recent conversation history in condensed format.

        Args:
            last_n: Number of recent exchanges to show
        """
        if not self.conversation_history:
            return
        
        print(f"\n{Style.DIM}{'─' * TEXT_WIDTH}")
        print(f"Recent conversation:{Style.RESET_ALL}")
        
        for user_input, response_dict in self.conversation_history[-last_n:]:
            sass = response_dict.get('sass_level', 5)
            response_preview = response_dict.get('response', '')[:50] + '...'
            
            print(f"{Style.DIM}  You: {user_input[:40]}{'...' if len(user_input) > 40 else ''}")
            print(f"  Derek [sass:{sass}]: {response_preview}{Style.RESET_ALL}")
        
        print(f"{Style.DIM}{'─' * TEXT_WIDTH}{Style.RESET_ALL}\n")

    def show_stats(self):
        """Show Derek's statistics."""
        avg_sass = self.total_sass / self.response_count if self.response_count > 0 else 0
        
        stats = f"""
{Style.BRIGHT}Derek's Session Statistics:{Style.RESET_ALL}
{Style.DIM}{'─' * TEXT_WIDTH}
Responses given: {self.response_count}
Average sass level: {avg_sass:.1f}/10
Total pedantry points: {self.total_sass}
Conversation length: {len(self.conversation_history)} exchanges
{'─' * TEXT_WIDTH}{Style.RESET_ALL}
"""
        print(stats)

    def show_help(self):
        """Show available commands."""
        help_text = f"""
{Style.BRIGHT}Available Commands:{Style.RESET_ALL}
{Style.DIM}{'─' * TEXT_WIDTH}
/sass     - Show sass-o-meter legend
/history  - Display recent conversation history
/stats    - Show Derek's session statistics
/help     - Show this help message
exit/quit - End the conversation
{'─' * TEXT_WIDTH}{Style.RESET_ALL}
"""
        print(help_text)

    def type_text(self, text: str, delay: float = 0.02, color: str = Fore.CYAN, 
                  vary_speed: bool = True):
        """Print text with typing effect and optional speed variation.

        Args:
            text: Text to print
            delay: Base delay between characters (seconds)
            color: Colorama color code
            vary_speed: Whether to vary typing speed for emphasis
        """
        import re
        
        if not sys.stdout.isatty():
            # Non-interactive mode, print normally
            wrapped = self.wrap_text(text)
            print(f"{color}{wrapped}{Style.RESET_ALL}")
            return

        # Wrap text before typing
        wrapped = self.wrap_text(text)
        
        # Start with default color
        sys.stdout.write(color)
        
        i = 0
        while i < len(wrapped):
            char = wrapped[i]
            
            # Check if we're at the start of an ANSI escape sequence
            if char == '\033' or char == '\x1b':
                # Find the end of the escape sequence (ends with 'm')
                escape_seq = ''
                j = i
                while j < len(wrapped) and wrapped[j] != 'm':
                    escape_seq += wrapped[j]
                    j += 1
                if j < len(wrapped):
                    escape_seq += wrapped[j]  # Include the 'm'
                    # Write the entire escape sequence at once
                    sys.stdout.write(escape_seq)
                    sys.stdout.flush()
                    i = j + 1
                    continue
            
            # Variable speed logic
            current_delay = delay
            if vary_speed:
                # Slow down for "ACTUALLY"
                if i < len(wrapped) - 8 and wrapped[i:i+8] == 'ACTUALLY':
                    current_delay = delay * 3  # Much slower for emphasis
                # Pause after punctuation
                elif char in '.!?':
                    current_delay = delay * 8
                elif char in ',;:':
                    current_delay = delay * 4
                # Faster through parenthetical asides
                elif char in '()':
                    current_delay = delay * 0.3
            
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(current_delay)
            i += 1
        
        # Reset at end
        sys.stdout.write(Style.RESET_ALL)
        print()  # Newline at end

    def format_response_text(self, text: str) -> str:
        """Format response text with emphasis on key phrases.

        Args:
            text: Response text

        Returns:
            Formatted text with color codes
        """
        import re
        
        # Emphasize "ACTUALLY" - Derek's signature word (slow typing too)
        text = text.replace('ACTUALLY', f'{Style.BRIGHT}{Fore.YELLOW}ACTUALLY{Style.RESET_ALL}{Fore.CYAN}')
        
        # Emphasize FACT in all caps
        text = text.replace('FACT:', f'{Style.BRIGHT}{Fore.RED}FACT:{Style.RESET_ALL}{Fore.CYAN}')
        
        # Highlight robot actions and asides (in asterisks)
        text = re.sub(
            r'\*(.*?)\*',
            f'{Style.DIM}{Fore.MAGENTA}*\\1*{Style.RESET_ALL}{Fore.CYAN}',
            text
        )
        
        # Highlight citations (author et al. pattern)
        text = re.sub(
            r'\b([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?(?:\s+et al\.)?)\s*\((\d{4})\)',
            f'{Fore.BLUE}\\1 (\\2){Fore.CYAN}',
            text
        )
        
        # Highlight technical terms (capitalized acronyms)
        text = re.sub(
            r'\b([A-Z]{2,})\b',
            f'{Style.BRIGHT}\\1{Style.RESET_ALL}{Fore.CYAN}',
            text
        )

        return text

    def _talking_animation_loop(self, sass_level: int):
        """Background thread for talking animation."""
        while self._talking_active:
            if self.animations:
                face = random.choice(self.animations.talking_faces)
                combined = self.animations.combine_meter_and_face(face, sass_level)

                # Update display
                if sys.stdout.isatty():
                    # Save cursor position, update face area, restore cursor
                    # For simplicity, we'll just show the animation at intervals
                    pass

            time.sleep(1.5)  # Change talking face every 1.5 seconds

    def get_llm_response(self, user_input: str) -> Dict:
        """Generate response using LLM with keyword context.

        Args:
            user_input: User's message

        Returns:
            Response dictionary with 'response' and 'sass_level'
        """
        if not self.llm_available or not self.llm_client:
            # Fall back to keyword matching
            return self.matcher.get_response(user_input)

        try:
            # Get top keyword matches for context
            matched_responses, suggested_sass = self.matcher.get_top_matches_for_llm(user_input, n=3)

            # Generate streaming response from LLM
            response_text = ""
            for token in self.llm_client.generate_streaming(
                user_input, matched_responses, suggested_sass
            ):
                response_text += token

            # Return response dict
            return {
                'response': response_text.strip(),
                'sass_level': suggested_sass,  # LLM might have adjusted this
                'llm_generated': True
            }

        except Exception as e:
            # Fall back to keyword matching on error
            print(f"\n{Fore.YELLOW}LLM error: {e}. Using keyword fallback.{Style.RESET_ALL}")
            return self.matcher.get_response(user_input)

    def display_response(self, response_dict: Dict):
        """Display Derek's response with personality and animations.

        Args:
            response_dict: Response dictionary from matcher or LLM
        """
        sass_level = response_dict.get('sass_level', 5)
        is_llm_generated = response_dict.get('llm_generated', False)

        # Update statistics
        self.response_count += 1
        self.total_sass += sass_level

        # Show thinking animation (keeps previous conversation visible)
        if self.animations:
            thinking_time = random.uniform(0.8, 1.5)
            self.animations.display_thinking_animation(sass_level, duration=thinking_time)

        # Determine face type based on sass level
        if sass_level >= 8:
            face_type = "sassy"
        else:
            face_type = "talking"

        # Display appropriate face (this will clear screen and show face)
        if self.animations:
            self.animations.display_face(face_type, sass_level)

        # Add separator line between face and response
        print(f"{Style.DIM}{'─' * TEXT_WIDTH}{Style.RESET_ALL}")
        print()

        # Get and format the main response
        response_text = response_dict.get('response', '')
        formatted_text = self.format_response_text(response_text)

        # Type out the response with label
        sass_indicator = self._get_sass_indicator(sass_level)
        print(f"{Fore.CYAN}Derek {sass_indicator}:{Style.RESET_ALL}")
        self.type_text(formatted_text, delay=0.015, color=Fore.CYAN, vary_speed=True)

        # Maybe show follow-up (50% chance if it exists and not LLM generated)
        if not is_llm_generated and 'follow_up' in response_dict and random.random() < 0.5:
            time.sleep(0.5)  # Brief pause
            print()  # Extra spacing before follow-up
            follow_up = response_dict['follow_up']
            formatted_followup = self.format_response_text(follow_up)
            self.type_text(formatted_followup, delay=0.015, color=Fore.CYAN, vary_speed=True)

        print()  # Extra newline for spacing

    def _get_sass_indicator(self, sass_level: int) -> str:
        """Get emoji indicator for sass level.

        Args:
            sass_level: Sass level 0-10

        Returns:
            Emoji string
        """
        if sass_level >= 9:
            return "🤓💥"  # Maximum pedantry
        elif sass_level >= 7:
            return "🤓"    # High confidence
        elif sass_level >= 5:
            return "📚"    # Moderate
        elif sass_level >= 3:
            return "🤖"    # Robot mild
        else:
            return "😊"    # Rare politeness

    def get_user_input(self) -> str:
        """Get input from user with styled prompt.

        Returns:
            User input string
        """
        try:
            print()  # Add spacing before prompt
            user_input = input(f"{Style.BRIGHT}{Fore.WHITE}You: {Style.RESET_ALL}")
            return user_input.strip()
        except EOFError:
            return "exit"

    def check_exit_command(self, user_input: str) -> bool:
        """Check if user wants to exit.

        Args:
            user_input: User's input

        Returns:
            True if should exit
        """
        exit_commands = {'exit', 'quit', 'bye', 'goodbye', 'q'}
        return user_input.lower() in exit_commands

    def run(self):
        """Run the main interactive loop."""
        # Show greeting with neutral face
        if self.animations:
            self.animations.display_face("neutral", sass_level=5)

        # Add separator
        print(f"{Style.DIM}{'─' * TEXT_WIDTH}{Style.RESET_ALL}")
        print()

        # Show LLM status
        print(f"{Style.DIM}{self.llm_status_msg}{Style.RESET_ALL}")
        print()

        print(f"{Fore.CYAN}Derek 😊:{Style.RESET_ALL}")
        greeting_response = self.matcher.get_response("", response_type='greeting')
        self.type_text(greeting_response['response'], delay=0.012, color=Fore.CYAN, vary_speed=False)
        print()

        # Show help hint
        print(f"{Style.DIM}Tip: Type /help for available commands{Style.RESET_ALL}\n")

        # Main loop
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()

                if not user_input:
                    continue

                # Check for commands
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                    continue

                # Check for exit
                if self.check_exit_command(user_input):
                    self._goodbye_sequence()
                    break

                # Get and display response (LLM-enhanced or keyword fallback)
                response = self.get_llm_response(user_input)
                print()  # Spacing
                self.display_response(response)

                # Store in history
                self.conversation_history.append((user_input, response))

            except KeyboardInterrupt:
                print("\n")
                self._goodbye_sequence()
                break
            except Exception as e:
                print(f"\n{Fore.RED}ERROR: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}System malfunction... Recovering...{Style.RESET_ALL}\n")
    
    def _handle_command(self, command: str):
        """Handle special commands.

        Args:
            command: Command string starting with /
        """
        cmd = command.lower().strip()
        
        if cmd == '/sass':
            self.show_sass_legend()
        elif cmd == '/history':
            self.show_conversation_history()
        elif cmd == '/stats':
            self.show_stats()
        elif cmd == '/help':
            self.show_help()
        else:
            print(f"{Fore.YELLOW}Unknown command: {command}{Style.RESET_ALL}")
            print(f"{Style.DIM}Type /help for available commands{Style.RESET_ALL}\n")
    
    def _goodbye_sequence(self):
        """Handle goodbye with sassy face."""
        print()
        if self.animations:
            # Show random sassy face for goodbye
            sassy_face = random.choice(self.animations.sassy_faces)
            sass_level = 8
            combined = self.animations.combine_meter_and_face(sassy_face, sass_level)
            
            if sys.stdout.isatty():
                os.system('clear' if os.name == 'posix' else 'cls')
            
            print(combined)
            print()
            print(f"{Style.DIM}{'─' * TEXT_WIDTH}{Style.RESET_ALL}")
            print()
        
        print(f"{Fore.CYAN}Derek 🤓:{Style.RESET_ALL}")
        goodbye_response = self.matcher.get_response("", response_type='goodbye')
        self.type_text(goodbye_response['response'], delay=0.012, color=Fore.CYAN, vary_speed=False)
        
        # Show final stats
        if self.response_count > 0:
            print()
            self.show_stats()
        
        print()


def main():
    """Main entry point for derek_mcp command."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Derek MCP - The Molecular Control Pedant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Derek is a pedantic PhD candidate bot specializing in molecular AI.
He will correct you with maximum confidence and minimum accuracy.

Commands during session:
  exit, quit, bye - Exit the session
  Ctrl+C          - Force exit
        """
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Derek MCP v0.1.0'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    args = parser.parse_args()

    if args.no_color and COLORS_AVAILABLE:
        # Disable colorama
        import colorama
        colorama.deinit()

    # Run Derek
    try:
        derek = DerekCLI()
        derek.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
