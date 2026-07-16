from flask import Flask, request, jsonify
from moviepy import TextClip, ColorClip, CompositeVideoClip
import os

app = Flask(__name__)

@app.route('/edit-video', methods=['POST'])
def edit_video():
    data = request.json or {}
    text_content = data.get('instructions', 'Hello from n8n!')
    
    try:
        # 1. Create a simple dark background clip (1280x720, 5 seconds long)
        bg_clip = ColorClip(size=(1280, 720), color=(30, 30, 30), duration=5)
        
        # 2. Add text directly using modern moviepy syntax (requires no ImageMagick)
        txt_clip = TextClip(
            text=text_content, 
            font_size=40, 
            color='white', 
            font='DejaVu-Sans'  # standard font present on Linux servers
        ).with_duration(5).with_position('center')
        
        # 3. Layer them together
        final_video = CompositeVideoClip([bg_clip, txt_clip])
        
        # Save the file locally on Render
        output_filename = "edited_video.mp4"
        final_video.write_videofile(output_filename, fps=24, codec="libx264")
        
        return jsonify({
            "status": "success", 
            "message": "Video rendered successfully!",
            "video_url": f"https://syntropy-c6tj.onrender.com/download/{output_filename}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Add an endpoint so n8n or users can download the actual video file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    from flask import send_from_directory
    return send_from_directory(os.getcwd(), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
