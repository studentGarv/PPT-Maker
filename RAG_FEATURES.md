# PPT Maker - RAG & Improvement Features

## New Features Added

### 📚 RAG (Retrieval-Augmented Generation)
The PPT Maker now supports using reference materials to create more informed presentations:

#### Supported Input Types:
- **PowerPoint files (.pptx)**: Extracts text content from slides
- **PDF files (.pdf)**: Extracts text from all pages
- **Text files (.txt, .md)**: Processes plain text content
- **URLs**: Fetches and extracts content from web pages

#### How RAG Works:
1. **Upload Reference Files**: Add PPT, PDF, or text files as context
2. **Provide URLs**: Include web links for additional context
3. **Enable RAG**: Check the "Enable RAG" option
4. **Generate**: The AI will use your reference materials to create a more informed presentation

#### Technical Implementation:
- Uses embedding-based similarity search (cosine similarity)
- Chunks documents into manageable pieces
- Retrieves most relevant content based on your prompt
- Enhances your original prompt with contextual information

### 🔧 Presentation Improvement
Analyze and enhance existing PowerPoint presentations:

#### Features:
- **Content Analysis**: Extracts and analyzes existing slide content
- **Deduplication**: Removes redundant or similar slides using embeddings
- **AI Enhancement**: Uses LLM to reorganize and improve content structure
- **Professional Output**: Creates cleaner, more concise presentations

#### How It Works:
1. **Upload PPT**: Select an existing PowerPoint file
2. **Choose Model**: Pick your preferred AI model
3. **Improve**: The system will analyze and enhance your presentation
4. **Download**: Get an improved version with better structure and flow

## Web Interface Updates

### Two Main Tabs:
1. **📄 Create New Presentation**: 
   - Original PPT generation functionality
   - Enhanced with RAG capabilities
   - File upload for reference materials
   - URL input for web-based context

2. **🔧 Improve Existing Presentation**:
   - Upload existing PPT files
   - AI-powered analysis and enhancement
   - Automatic content optimization

### RAG Configuration:
- **Enable/Disable**: Toggle RAG functionality on/off
- **Multiple File Upload**: Support for various file types
- **URL Processing**: Extract content from web sources
- **Status Feedback**: Real-time information about processed materials

## Security Improvements
- Replaced MD5 hashing with SHA-256 for better security
- Secure content processing and caching

## Usage Examples

### Creating a Presentation with RAG:
1. Enter your topic: "Machine Learning in Healthcare"
2. Upload reference files: research papers, existing presentations
3. Add URLs: relevant articles, documentation
4. Enable RAG and generate presentation
5. Download your context-aware presentation

### Improving an Existing Presentation:
1. Go to "Improve Existing Presentation" tab
2. Upload your current PowerPoint file
3. Select AI model for analysis
4. Click "Improve Presentation"
5. Download the enhanced version

## Technical Details

### Dependencies Added:
- `PyPDF2`: PDF text extraction
- `requests`: URL content fetching
- `ollama`: AI model integration for embeddings and generation

### Key Components:
- `rag_processor.py`: Core RAG functionality
- `ppt_improver.py`: Presentation improvement logic
- Enhanced `web_app.py`: Updated UI with new features

### Models Used:
- **Generation**: gpt-oss:20b (default), llama3, mistral, or custom models
- **Embeddings**: nomic-embed-text (default)
- **Configurable**: All models can be changed in the interface

## Getting Started

1. **Start Ollama**: Make sure Ollama is running (`ollama serve`)
2. **Install Models**: 
   ```bash
   ollama pull gpt-oss:20b
   ollama pull nomic-embed-text
   ```
3. **Run Web App**: `python web_app.py`
4. **Access Interface**: http://localhost:7860

The enhanced PPT Maker now provides comprehensive presentation creation and improvement capabilities with AI-powered context awareness!
