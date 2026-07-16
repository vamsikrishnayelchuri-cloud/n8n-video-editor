from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os

app = Flask(__name__)

@app.route('/edit-video', methods=['POST'])
def edit_video():
    data = request.json or {}
    text_content = data.get('instructions', 'Hello from n8n!')
    
    try:
        # Create a simple 5-second video with your text instructions overlaid
        txt_clip = TextClip(text_content, fontsize=50, color='white', size=(1280, 720))
        txt_clip = txt_clip.set_duration(5)
        
        # Save the file locally on your Render instance
        output_filename = "edited_video.mp4"
        txt_clip.write_videofile(output_filename, fps=24, codec="libx264")
        
        # For testing, we return a success status
        return jsonify({
            "status": "success", 
            "message": "Video rendered successfully!",
            "video_url": "https://your-app.onrender.com/download/edited_video.mp4"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
