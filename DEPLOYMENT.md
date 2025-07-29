# PPT Maker - Deployment Guide for Non-Technical Users

This guide shows you how to make PPT Maker available to users who don't have Python or Ollama installed.

## 🎯 **Deployment Options**

### **Option 1: Standalone Executable (Easiest for Windows)**

**For Users:** No installation required, just download and run!

**How to Create:**
1. Run `build_executable.bat` on a machine with Python
2. Share the `dist\PPT-Maker.exe` file
3. Users need to install Ollama separately

**User Instructions:**
```bash
# 1. Download and install Ollama
# Visit: https://ollama.ai/download

# 2. Start Ollama and download model
ollama serve
ollama pull llama3

# 3. Run PPT Maker
PPT-Maker.exe "Create a presentation about AI"
```

---

### **Option 2: Web Application (Best for Multiple Users)**

**For Users:** Access through web browser - no installation needed!

**How to Deploy:**
1. Install requirements: `pip install -r requirements_web.txt`
2. Run: `python web_app.py`
3. Share the web URL with users

**User Instructions:**
- Open web browser
- Go to the provided URL
- Enter presentation topic and generate

---

### **Option 3: Portable Package (Complete Solution)**

**For Users:** Everything included in one folder!

**How to Create:**
1. Run `create_portable.bat`
2. Follow the generated README.md to complete setup
3. Share the entire `PPT-Maker-Portable` folder

**User Instructions:**
- Extract the portable folder
- Double-click `PPT-Maker.bat`
- No installation required!

---

### **Option 4: Cloud Deployment (Enterprise Solution)**

**For Organizations:** Deploy on cloud servers for company-wide access

**How to Deploy:**
```bash
# Using Docker
docker-compose up -d
```

**User Instructions:**
- Access through company intranet
- Use web interface
- No local installation needed

---

### **For Individual Users (Executable):**
```bash
# Creator:
build_executable.bat
# User:
# 1. Install Ollama
# 2. Run PPT-Maker.exe "your topic"
```

### **For Small Teams (Web App):**
```bash
# Creator:
python web_app.py
# Users:
# Open browser -> http://your-server:7860
```

### **For Offline Distribution (Portable):**
```bash
# Creator:
create_portable.bat
# Follow setup instructions

# Users:
# Extract folder -> Run PPT-Maker.bat
```

### **For Enterprise (Cloud):**
```bash
# IT Department:
docker-compose up -d

# Employees:
# Access company intranet URL
```

---