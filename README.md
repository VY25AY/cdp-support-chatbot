# CDP Support Chatbot

A web-based chatbot that answers "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot extracts relevant information from official documentation to guide users on performing tasks within each platform.

## Features

### Core Functionalities

1. **Answer "How-to" Questions**
   - Handles questions about specific tasks in each CDP
   - Provides step-by-step instructions from documentation
   - Example: "How do I set up a new source in Segment?"

2. **Documentation Information Extraction**
   - Efficiently extracts relevant information from stored documentation
   - Uses intelligent keyword matching with related terms
   - Handles variations in question phrasing

3. **Question Variation Handling**
   - Handles different question formats and lengths
   - Uses expanded keyword matching for better understanding
   - Filters out irrelevant questions

### Bonus Features

1. **Cross-CDP Comparisons**
   - Compare features across different CDPs
   - Side-by-side comparison of procedures
   - Example: "How does Segment's audience creation compare to Lytics?"

2. **Advanced Question Handling**
   - Support for complex queries about platform-specific features
   - Detailed responses for advanced configurations
   - Multiple CDP handling in a single query

## Project Structure

```
cdp_chatbot/
├── app.py                 # Main Flask application
├── chatbot.py            # Core chatbot logic
├── requirements.txt      # Python dependencies
├── docs/                 # Documentation files
│   ├── segment.txt
│   ├── mparticle.txt
│   ├── lytics.txt
│   └── zeotap.txt
├── templates/
│   └── index.html       # Chat interface template
└── static/
    ├── css/
    │   └── style.css    # UI styling
    └── js/
        └── script.js    # Frontend functionality
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cdp-support-chatbot.git
   cd cdp-support-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the chatbot:
   - Open your browser and navigate to `http://127.0.0.1:5000`
   - Start asking questions about the supported CDPs

## Example Questions

1. Basic how-to questions:
   - "How do I set up a new source in Segment?"
   - "How can I create a user profile in mParticle?"
   - "How do I build an audience segment in Lytics?"
   - "How can I integrate my data with Zeotap?"

2. Comparison questions:
   - "How does Segment's audience creation compare to Lytics?"
   - "What's the difference between mParticle and Segment source setup?"

## Technical Details

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Documentation**: Text-based storage with intelligent retrieval
- **Features**:
  - Real-time chat interface
  - Intelligent keyword matching
  - Cross-CDP comparison support
  - Error handling and response validation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
