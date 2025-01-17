# Decentralized Autonomous Movie Creation System

This project is an AI-powered decentralized autonomous movie creation system. It uses GPT-2 for script generation, Streamlit for the user interface, and gTTS for converting scripts to audio. The system also includes a talent matchmaking feature to find the right talent based on required skills.

## Features
- **AI-Powered Script Generator:** Generate longer movie script snippets based on user-provided prompts.
- **Talent Matchmaking:** Match talents based on required skills such as acting, directing, editing, animation, VFX, and voiceover.
- **Text-to-Audio Conversion:** Convert generated scripts to audio files using gTTS.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    ```
2. Navigate to the project directory:
    ```sh
    cd your-repo-name
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the app.

## Project Structure
- `app.py`: The main Streamlit app file.
- `requirements.txt`: List of required Python packages.

## Script Generation
The script generation feature uses GPT-2 to create movie script snippets based on user-provided prompts. The generated scripts can be customized with a selectable script length.

## Talent Matchmaking
The talent matchmaking feature allows users to find the right talent based on required skills. Talents are listed with their name, skills, and portfolio URL.

## Text-to-Audio Conversion
The text-to-audio conversion feature uses gTTS to convert the generated scripts to audio files. Users can download the audio files directly from the app.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Contact
For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).
