import os
from os.path import isfile, join

def generate_html(name, pdf_files, audio_files, image_files):
    """
    Generate an HTML file that embeds multiple PDFs, adds buttons to control MP3 files, and displays static images.

    :param pdf_files: List of PDF file paths.
    :param audio_files: List of MP3 file paths.
    :param image_files: List of image file paths (JPG, PNG, etc.).
    """
    output_html = name+".html"
    # Start building the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{name}</title>
        <style>
            body {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
            }}
            .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 1px solid #ccc;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            padding: 15px;
            background-color: #f9f9f9;
            width: auto;  /* Define width */
            height: auto;  /* Allow height to adjust */
            text-align: center;
            position: absolute;
            resize: both;
            overflow: auto;
            }}
            iframe {{
                width: 100%;
                height: 100%;
                object-fit: contain;
            }}
            img {{
                max-width: 100%;
                height: auto;
                border: 1px solid #ccc;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            button {{
                margin: 5px;
                padding: 10px 15px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
        </style>
        <script>
            document.addEventListener("DOMContentLoaded", () => {{
                const containers = document.querySelectorAll(".container");

                containers.forEach(container => {{
                    let isDragging = false;
                    let isResizing = false;
                    let startX, startY, startWidth, startHeight;

                    // Dragging functionality
                    container.addEventListener("mousedown", (e) => {{
                        if (e.target === container) {{
                            isDragging = true;
                            let shiftX = e.clientX - container.getBoundingClientRect().left;
                            let shiftY = e.clientY - container.getBoundingClientRect().top;

                            const moveAt = (pageX, pageY) => {{
                                container.style.left = pageX - shiftX + 'px';
                                container.style.top = pageY - shiftY + 'px';
                            }};

                            const onMouseMove = (e) => {{
                                if (isDragging && !isResizing) {{
                                    moveAt(e.pageX, e.pageY);
                                }}
                            }};

                            document.addEventListener("mousemove", onMouseMove);

                            document.addEventListener("mouseup", () => {{
                                isDragging = false;
                                document.removeEventListener("mousemove", onMouseMove);
                            }}, {{ once: true }});
                        }}
                    }});

                    // Resizing functionality
                    container.addEventListener("mousedown", (e) => {{
                        if (e.target === container && e.offsetX > container.clientWidth - 10 && e.offsetY > container.clientHeight - 10) {{
                            isResizing = true;
                            startX = e.clientX;
                            startY = e.clientY;
                            startWidth = parseInt(document.defaultView.getComputedStyle(container).width, 10);
                            startHeight = parseInt(document.defaultView.getComputedStyle(container).height, 10);

                            const onMouseMove = (e) => {{
                                if (isResizing) {{
                                    container.style.width = startWidth + e.clientX - startX + 'px';
                                    container.style.height = startHeight + e.clientY - startY + 'px';
                                }}
                            }};

                            document.addEventListener("mousemove", onMouseMove);

                            document.addEventListener("mouseup", () => {{
                                isResizing = false;
                                document.removeEventListener("mousemove", onMouseMove);
                            }}, {{ once: true }});
                        }}
                    }});

                    container.ondragstart = () => false;
                }});
            }});
        </script>
    </head>
    <body>
        <h1 style="width: 100%; text-align: center;">{name}</h1>
    """

    # Add each PDF as an iframe
    for pdf in pdf_files:
        if os.path.exists(pdf):
            html_content += f"""
            <div class="container" style="left: 0; top: 0;">
                <iframe src="{pdf}" frameborder="0"></iframe>
            </div>
            """
        else:
            print(f"Warning: File not found - {pdf}")

    # Add controls for each MP3 file
    for audio in audio_files:
        if os.path.exists(audio):
            html_content += f"""
            <div class="container" style="left: 0; top: 0;">
                <p style="padding: 0px; margin: 0px;">{audio}</p>
                <audio id="{os.path.basename(audio)}" src="{audio}" controls></audio>
            </div>
            """
        else:
            print(f"Warning: File not found - {audio}")

    # Add each image as an <img> tag
    for image in image_files:
        if os.path.exists(image):
            html_content += f"""
            <div class="container" style="left: 0; top: 0;">
                <img src="{image}" alt="{os.path.basename(image)}">
            </div>
            """
        else:
            print(f"Warning: File not found - {image}")

    # Close the HTML content
    html_content += """
    </body>
    </html>
    """

    # Write the content to the output file
    with open(output_html, "w") as f:
        f.write(html_content)

    print(f"HTML file generated: {output_html}")

# Example usage
if __name__ == "__main__":
    name = input("File name?\n")
    path = input("\nFolder path? (Use '\\\\')\n")
    pdf_files = [f for f in os.listdir(path) if (isfile(join(path, f)) and f.split('.')[1] == "pdf")]  # Replace with your PDF file paths
    audio_files = [f for f in os.listdir(path) if (isfile(join(path, f)) and f.split('.')[1] == "mp3")]  # Replace with your MP3 file paths
    image_files = [f for f in os.listdir(path) if ((isfile(join(path, f)) and f.split('.')[1] == "png") or (isfile(join(path, f)) and f.split('.')[1] == "jpeg") or (isfile(join(path, f)) and f.split('.')[1] == "jpg") or (isfile(join(path, f)) and f.split('.')[1] == "webp"))]  # Replace with your image file paths

    generate_html(name,pdf_files, audio_files, image_files)
