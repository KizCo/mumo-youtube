# mumo-youtube
Mumo module for Mumble 1.5+ that parses YouTube links in text chat and fetches video titles using the open oEmbed API fallback.  
<img width="712" height="61" alt="image" src="https://github.com/user-attachments/assets/7f6bd35b-0502-4a6e-9be6-91efb49650f1" />


---

## ✨ Features
* **No API Key Required**: Uses YouTube's public oEmbed endpoint—no Google Developer tokens or configurations needed.
* **HTML-Safe Parsing**: Automatically cleans up the rich HTML markup embedded by Mumble clients to extract exact video IDs.
* **Fail-Safe Fallback**: If the primary API endpoint fails, the module safely drops back to a native web scraper to read the webpage `<title>` tag directly.
* **Duplicate Prevention**: Filters out duplicate links sent in the same text message block.

---

## 🛠️ Installation

### 1. Save the Module
Copy `youtube.py` into your primary Mumo `modules/` directory.

### 2. Enable the Module
Depending on how your Mumo environment is configured, choose **one** of the methods below:

#### Method A: If your setup uses a single `mumo.ini` file
Open your `mumo.ini` file and add `youtube` to your active modules list, then append the configuration at the bottom:
```ini
[modules]
youtube =

[youtube]
enabled = true
```

#### Method B: If your setup uses a `modules-enabled/` directory
Create a new file called `youtube.ini` inside your `modules-enabled/` folder:
```ini
[youtube]
enabled = true
```

### 3. Restart Mumo
Restart your Mumo bot framework instance to load the new extension.

---

## ⚙️ Compatibility
* Works natively with **Mumble 1.4.x / 1.5.x+** server deployments.
* Written using the standardized `mumo_module` namespace layer.

---

## 📄 License
This project is open-source and available under the terms of the MIT License.
