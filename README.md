# Videoist - Chinese Podcast Creator for Language Learners

Videoist is a powerful tool that helps Chinese language learners transform their creative content into Chinese-subtitled podcasts. The tool enables users to create engaging video content with automated Chinese subtitles, making it easier for learners to practice listening and reading skills simultaneously.

## Key Features

- **AI-Powered Content Creation**: Automatically generate scripts, titles, and subtitles from your text content
- **Multi-Platform Publishing**: Publish directly to WordPress sites and WeChat Official Accounts
- **Voice Synthesis**: Create natural-sounding Chinese audio with multiple voice options
- **Video Generation**: Automatically generate videos with synchronized subtitles
- **Content Repurposing**: Transform articles and text into engaging video content

## How It Helps Chinese Language Learning

Participating in Chinese social media through Videoist provides significant benefits for Chinese language learners:

1. **Authentic Content Creation**: Practice writing and expressing ideas in Chinese while creating real content
2. **Multimodal Learning**: Combine reading, listening, and viewing for enhanced language retention
3. **Cultural Engagement**: Connect with Chinese-speaking communities through authentic content
4. **Practical Application**: Use Chinese in real-world contexts rather than just academic exercises
5. **Portfolio Building**: Create a portfolio of Chinese content that demonstrates language proficiency
6. **Chinese LLM**: I encourage everyone to use domestic Chinese LLMs(deepseek/qwen/...), as they are better adapted to the content compliance requirements of the Chinese internet.

## Deployment Instructions

### Backend Setup

1. Create a new directory and clone the repository:
   ```bash
   sudo -u www git clone https://github.com/kindlyted/videoist .
   ```

2. Create an `.env` file and modify environment variables for production:
   ```bash
   cp .env.example .env
   # Edit .env file to set production values
   ```

3. Modify the `ALLOWED_ORIGINS` in the environment file to match your frontend domain

4. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. Check Gunicorn version (should be 23.0.0 as specified in requirements):
   ```bash
   gunicorn --version
   ```


### Frontend Setup

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

## Project Structure

- `app.py`: Main Flask application
- `models.py`: Database models
- `routes/`: API endpoints
- `services/`: Business logic and core functionality
- `frontend/`: Vue.js frontend application
- `storage/`: Storage for generated content
- `static/`: Static assets and templates
- `requirements.txt`: Python dependencies

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy, JWT
- **Frontend**: Vue.js 3, Pinia, Vue Router, Tailwind CSS
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI Services**: OpenAI API, DashScope
- **Deployment**: Gunicorn, Nginx

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.