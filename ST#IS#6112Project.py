import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tempfile
import webbrowser
import os
import random
import string


class ImageSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")

        root.title("Image Steganography")
        root.geometry("449x396")
        root.configure(bg="black")
        label_header = tk.Label(root, text="Image Steganography", font=("Helvetica", 16), bg="black", fg="white")
        label_header.pack(pady=10)

        frame_buttons = tk.Frame(root, bg="grey")
        frame_buttons.pack(pady=10)

        button_project_info = tk.Button(frame_buttons, text="Project Info", bg="red", fg="white",
                                        command=self.project_info, font=("Arial", 12, "bold"), width=10)
        button_project_info.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.lock_image = Image.open("lock_image.png").resize((200, 200))
        self.lock_photo = ImageTk.PhotoImage(self.lock_image)
        self.lock_label = tk.Label(root, image=self.lock_photo, bg="black")
        self.lock_label.pack()

        frame_buttons = tk.Frame(root, bg="grey")
        frame_buttons.pack(pady=10)

        button_hide_text = tk.Button(frame_buttons, text="Hide Text", font=("Arial", 12, "bold"), bg="red", fg="white",
                                     command=self.hide_text, width=10)
        button_hide_text.grid(row=1, column=0, padx=10, pady=10)

        button_extract_text = tk.Button(frame_buttons, text="Extract Text", bg="red", fg="white",
                                        command=self.extract_text,
                                        font=("Arial", 12, "bold"), width=10)
        button_extract_text.grid(row=1, column=1, padx=10, pady=10)

        self.encrypted_text = None  # Initialize encrypted_text variable

    


    def hide_text(self):
        image_path = filedialog.askopenfilename(title="Select Image to Hide Text")
        if image_path:
            image = Image.open(image_path)
            text = simpledialog.askstring("Enter Text", "Enter text to hide:")
            if text:
                # Fernet encryption
                key = Fernet.generate_key()
                cipher_suite = Fernet(key)
                self.encrypted_text = cipher_suite.encrypt(text.encode())  # Store encrypted text

                # Generate random OTP
                otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

                # Code to hide text in image
                # Save image
                save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                if save_path:
                    image.save(save_path)

                    # Send key and OTP to email address
                    email = simpledialog.askstring("Email Address", "Enter your email address:")
                    if email:
                        self.send_email(email, key.decode(), otp)
                        messagebox.showinfo("Success",
                                            "Text hidden and image saved successfully. Key and OTP sent to email.")
                    else:
                        messagebox.showwarning("Warning", "Email address is required.")
                else:
                    messagebox.showwarning("Warning", "Save path is required.")
            else:
                messagebox.showwarning("Warning", "Text is required.")

    def extract_text(self):
        if self.encrypted_text:  # Check if encrypted text is available
            image_path = filedialog.askopenfilename(title="Select Image to Extract Text")
            if image_path:
                # Key and OTP verification from email
                key = simpledialog.askstring("Enter Key", "Enter the key received in email:")
                if key:
                    otp = simpledialog.askstring("Enter OTP", "Enter the OTP received in email:")
                    if otp:
                        # Fernet decryption
                        cipher_suite = Fernet(key.encode())
                        # Code to decrypt text from image
                        extracted_text = cipher_suite.decrypt(self.encrypted_text).decode()
                        self.show_extracted_text(extracted_text)
                    else:
                        messagebox.showwarning("Warning", "OTP is required.")
                else:
                    messagebox.showwarning("Warning", "Key is required.")
        else:
            messagebox.showwarning("Warning", "No encrypted text available.")

    def show_extracted_text(self, text):
        top = tk.Toplevel(self.root)
        top.title("Extracted Text")
        text_widget = ScrolledText(top, wrap="word")
        text_widget.insert(tk.END, text)
        text_widget.pack(fill="both", expand=True)

    def project_info(self):
        file_html = '''  
        <!DOCTYPE html>
        <html>
        <head>
        <title>Project Details</title>
        <style>
        body{ 
        font-size:17px;
        }
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
          border-color:dark black;
        }
        </style>
        </head>
        <body>
           <h2> <center>PROJECT INFORMATION</center> </h2>        
        <center><h1>Image Steganography</h1></center>
        <center> <table style="width:40%">
          <tr>
            <th><b>Project Details</b></th>
            <th>Value</th> 
          </tr>
          <tr>
            <td>Project Name</td>
            <td>Image Steganography</td>
          </tr>
          <tr>
            <td>Project Description</td>
            <td>Implementing to conceal secret data within an image without altering its visual appearance.</td>
          </tr>
          <tr>
            <td>Project Start Date</td>
            <td>17-02-2024</td>
          </tr>
          <tr>
            <td>Project End Date</td>
            <td>17-03-2024</td>
          </tr>
          <tr>
            <td>Project Status</td>
            <td><b>Completed</b></td>
          </tr>
        </table>
        </center>
        <h3><center>Developer Details</center></h3>
        <center> <table style="width:40%">
                  <tr>
            <th><b>Name</b></th>
            <th>Email</th> 
          </tr>
          <tr>
            <td>ST3IS#6108</td>
            <td>jyothish@gmail.com</td>
          </tr>
           <tr>
            <td>ST3IS#6110</td>
            <td>sathvik@gmail.com</td>
          </tr>
          <tr>
            <td>ST3IS#6111</td>
            <td>keertan@gmail.com</td>
          </tr>
          <tr>
            <td>ST3IS#6112</td>
            <td>devisrinivas@gmail.com</td>
          </tr>
          <tr>
            <td>ST3IS#6113</td>
            <td>vineetha@gmail.com</td>
          </tr>
        </table>
        </center>

        </table>
        </center>
        <h3><center>Company Details</center></h3>
        <center> <table style="width:40%">
          <tr>
            <th><b>Company</b></th>
            <th>Contact Email</th> 
          </tr>
          <tr>
            <td>Name</td>
            <td>Anonymous Cyber Solutions</td>
          </tr>
          <tr>
            <td>Email</td>
            <td>contact@stegnos.com</td>
          </tr>
        </table>
        </center>

        </body>
        </html>'''

        # Saving the data into the HTML file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as temp_file:
            temp_file.write(file_html)
            temp_file_path = temp_file.name

        # Opening HTML file in a web browser window
        webbrowser.open("file://" + os.path.realpath(temp_file_path))

    def send_email(self, recipient_email, key, otp):
        sender_email = "keertan224@gmail.com"  # Update with your email
        password = "xtutydhjpgorktpa"
        # Update with your email password

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Key and OTP for Image Steganography"

        body = f"Here is the key to decrypt the hidden text: {key}\n\nOTP: {otp}"
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSteganographyApp(root)
    root.mainloop()

