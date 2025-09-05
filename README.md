# 🎵 Videoist - Chinese Podcast Creator for Language Learners 🎵

Videoist is a powerful tool that helps Chinese language learners transform their creative content into Chinese-subtitled podcasts. The tool enables users to create engaging video content with automated Chinese subtitles, making it easier for learners to practice listening and reading skills simultaneously.

## 🌟 Key Features

- **🤖 AI-Powered Content Creation**: Automatically generate scripts, titles, and subtitles from your text content
- **📱 Multi-Platform Publishing**: Publish directly to WordPress sites and WeChat Official Accounts
- **🗣️ Voice Synthesis**: Create natural-sounding Chinese audio with multiple voice options
- **🎬 Video Generation**: Automatically generate videos with synchronized subtitles
- **🔄 Content Repurposing**: Transform articles and text into engaging video content

## 🎓 How It Helps Chinese Language Learning

Participating in Chinese social media through Videoist provides significant benefits for Chinese language learners:

1. **✍️ Authentic Content Creation**: Practice writing and expressing ideas in Chinese while creating real content
2. **🧠 Multimodal Learning**: Combine reading, listening, and viewing for enhanced language retention
3. **🌏 Cultural Engagement**: Connect with Chinese-speaking communities through authentic content
4. **💼 Practical Application**: Use Chinese in real-world contexts rather than just academic exercises
5. **📚 Portfolio Building**: Create a portfolio of Chinese content that demonstrates language proficiency
6. **🇨🇳 Chinese LLM**: I encourage everyone to use domestic Chinese LLMs(deepseek/qwen/...), as they are better adapted to the content COMPLIANCE requirements of the Chinese internet. Because your articles may contain sensitive words, using Google Notebook LM might lead to rejection of publication, lengthy review processes, traffic restrictions, etc. This is the reason why I recommend using Chinese language models.

## 🌐 Demo Website - https://www.ai4uo.com

```
┌─────────────────────────────────────────────────────────────┐
│  Follow these steps to get started with Videoist:           │
└─────────────────────────────────────────────────────────────┘
```

1. 📝 Register an account
2. 🔧 Add your WordPress site and WeChat Official Account (you can skip this step if you don't need to publish to WordPress or WeChat)
   - 2.1 For WordPress sites, you need your username and password, as well as the WordPress site's URL/tag/categories (it's highly recommended to only use this feature when deploying locally)
   - 2.2 The WeChat Official Account publishing API is no longer available to the public. You need to apply for a corporate account and complete authentication. This may not be suitable for individual bloggers
3. 🎧 Generate your podcast script
   - 3.1 Copy your blog post URL or the full article text into the input box (you can also paste news URLs you're interested in, but please note the website's anti-crawling mechanisms)
   - 3.2 Click the upload button
   - 3.3 Wait for the script generation to complete. The generated script will be displayed below the input box
   - 3.4 You can edit the script and click the save button to save it
   - 3.5 Click the generate title button
   - 3.6 Select a voice you like, then click the generate button
   - 3.7 Wait for the video generation to complete. The video will be displayed below
   - 3.8 Publish to Douyin, Xiaohongshu, and Shipinhao platforms (the demo website's server cannot do this, so local deployment only)

## 🚀 Deployment Instructions

### 🖥️ Backend Setup

1. Create a new directory and clone the repository:
   ```bash
   # For local deployment, you can directly download and extract to the specified folder
   sudo -u www git clone https://github.com/kindlyted/videoist .
   ```

2. Create an `.env` file and modify environment variables for production:
   ```
   # API key for the large language model you need, here I recommend deepseek's API
   API_KEY="yourkey"
   BASE_URL="https://api.deepseek.com"
   API_KEY_KIMI="yourkey"
   URL_KIMI="https://api.moonshot.cn/v1"
   API_KEY_QWEN="yourkey"
   URL_QWEN="https://dashscope.aliyuncs.com/compatible-mode/v1"
   # If you want to use the WordPress site and WeChat official account publishing feature, you need to apply for an Unsplash API key
   UNP_AKEY="yourkey"
   UNP_SKEY="yourkey"
   UNP_ID="726776"
   # API key for the large language model you need, here I recommend deepseek's API
   SECRET_KEY=your-key
   JWT_SECRET_KEY=your-key
   PYTHONPATH="your-project-path"
   FLASK_APP=app.py
   FLASK_ENV=development
   # Modify the `ALLOWED_ORIGINS` in the environment file to match your frontend domain
   ALLOWED_ORIGINS=http://localhost:5173
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Install ffmpeg and add its path to the environment variables

5. Check Gunicorn version (should be 23.0.0 as specified in requirements):
   ```bash
   # For local deployment, you don't need to check the gunicorn version
   gunicorn --version
   ```

6. Start the backend
   ```bash
   $env:PYTHONPATH = "$PWD;$env:PYTHONPATH"
   $env:FLASK_APP = "app.py"
   flask db upgrade # Only needed for the first deployment
   flask run --host=0.0.0.0 --port=5010 --debug
   ```

### 🌐 Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the production frontend:
   ```bash
   npm run build
   ```
4. Start the frontend
   ```bash
   npm run dev
   ```
5. Access the website
   ```
   http://localhost:5173
   ```
## 📁 Project Structure

```
videoist/
├── app.py              # Main Flask application
├── models.py           # Database models
├── routes/             # API endpoints
├── services/           # Business logic and core functionality
├── frontend/           # Vue.js frontend application
├── storage/            # Storage for generated content
├── static/             # Static assets and templates
└── requirements.txt    # Python dependencies
```

## 🛠️ Technologies Used

- **Backend**: Python, Flask, SQLAlchemy, JWT
- **Frontend**: Vue.js 3, Pinia, Vue Router, Tailwind CSS
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI Services**: OpenAI API, DashScope
- **Deployment**: Gunicorn, Nginx

## ⚠️ Limitations and Future Plans
- I haven't done software engineering and don't know how to write documentation. This document was written by QWEN, and I will gradually improve it.
- I'm not sure if the MIT license is appropriate.
- Currently, only video publishing on three platforms is supported: Douyin, Xiaohongshu, and Shipinhao. Other platforms will be added gradually.
- Next step is to add a translation feature for "memes" on the Simplified Chinese internet.
- Next step is to create a community about the Simplified Chinese internet.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.