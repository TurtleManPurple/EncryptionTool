# 📥 How to Install EncryptionTool on Mac

Because this app is independently developed, macOS requires a quick manual step to verify and unlock it after downloading. Follow these simple steps to install and run the app.

---

### Step 1: Install the Application
1. Double-click the downloaded file named **`EncryptionToolInstaller.dmg`** to open it.
2. A window will pop up showing the **EncryptionTool** icon. 
3. **Drag and drop** the **EncryptionTool** icon directly into the **Applications** folder shortcut inside that window.
4. Close the installer window.

---

### Step 2: Unlock the Application (One-Time Step)
Mac computers automatically lock apps downloaded from the internet. To unlock it, follow these quick steps:

1. Open your Mac's **Terminal** app:
   * Press the **`Command (⌘)` key** and the **Spacebar** at the same time to open the search bar.
   * Type **`Terminal`** and press **Enter**.
2. Copy the exact line of text below, paste it into the Terminal window, and press **Enter**:

   ```bash
   sudo xattr -cr /Applications/EncryptionTool.app
   ```

3. Terminal will ask for your **Mac Login Password** (the password you use to unlock your computer when you turn it on):
   * Type your password and press **Enter**.
   * *Note: Terminal hides your password as you type for security. No characters, stars, or dots will show on the screen. Just type it blindly and hit Enter!*

---

### 🎉 All Done!
You can now close the Terminal. Open your **Applications** folder or **Launchpad** and double-click **EncryptionTool** to open the application normally!
