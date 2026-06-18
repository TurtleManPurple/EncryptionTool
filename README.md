# 📥 How to Install EncryptionTool on Mac

Because this app is independently developed, macOS requires a quick manual step to verify and unlock it after downloading. Follow these simple steps to install and run the app.

---

### Step 1: Install the Application
1.Download **`EncryptionToolInstaller.dmg`**
2. Double-click the downloaded file named **`EncryptionToolInstaller.dmg`** to open it.
3. A window will pop up showing the **EncryptionTool** icon. 
4. **Drag and drop** the **EncryptionTool** icon directly into the **Applications** folder shortcut inside that window.
5. Close the installer window.

---

### Step 2: Unlock the Application (One-Time Step)
Mac computers automatically lock apps downloaded from the internet. To unlock it, follow these quick steps:

1. Open your Mac's **Terminal** app:
   * Press the **`Command (⌘)` key** and the **Spacebar** at the same time to open the search bar.
   * Type **`Terminal`** and press **Enter**.
2. Copy the exact line of text below, paste it into the Terminal window, and press **Enter**:

   ```bash
   xattr -cr /Applications/EncryptionTool.app
   ```

---

### 🎉 All Done!
You can now close the Terminal. Open your **Applications** folder or **Launchpad** and click **EncryptionTool** to open the application normally!
