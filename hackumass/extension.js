const vscode = require('vscode');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Define a global decoration type
const decorationType = vscode.window.createTextEditorDecorationType({
    backgroundColor: 'rgba(255,255,0,0.3)',
});

// Function to send the active file and folder content to the backend
async function sendFileAndFolderToBackend() {
    vscode.window.showInformationMessage('Hello World from hackumass!');

    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage("No active editor found!");
        return;
    }

    const document = editor.document;
    const fileContent = document.getText();
    const current_fileName = document.fileName;
    console.log(fileContent);

    const folderUri = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri : null;

    if (!folderUri) {
        vscode.window.showErrorMessage("No folder is currently open in the workspace.");
        return;
    }

    // Read all files in the folder
    const folderContent = await readFolderContents(folderUri.fsPath);

    try {
        // Send the file content and folder content to the backend
        const response = await axios.post('http://localhost:5000/process', {
            fileContent,
            folderContent,
            current_fileName
        });
        //console.log("RESSSPONSSSEEE")
        console.log("response.data: ",response.data);

        if (response.data && response.data.highlights) {
            highlightLinesAndSuggestions(response.data.highlights);
        }

        if (response.data && response.data.folderInsights) {

        }
    } catch (error) {
        vscode.window.showErrorMessage("Error communicating with the backend: " + error.message);
    }
}

// Function to read all files in the folder recursively
async function readFolderContents(folderPath) {
    const files = fs.readdirSync(folderPath, { withFileTypes: true });
    const folderContent = {};

    for (const file of files) {
        const fullPath = path.join(folderPath, file.name);

        if (file.isDirectory()) {
            folderContent[file.name] = await readFolderContents(fullPath);
        } else if (file.isFile() && path.extname(file.name) === ".py") {
            folderContent[file.name] = fs.readFileSync(fullPath, 'utf-8');
        }
    }

    return folderContent;
}

// Function to highlight lines and show suggestions
function highlightLinesAndSuggestions(highlights) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    let longDecorations = [];
    let unusedDecorations = [];

highlights.forEach(({ tag, suggestion, start_line, end_line, line }) => {
    if (tag === "long" || tag === "multiple_duplicate") {
        console.log("in longgg", highlights);
        // If tag is 'long', handle the long function body decoration
        const decorations = {
            range: new vscode.Range(start_line - 1, 0, end_line - 1, 100), // Use both start and end lines
            hoverMessage: suggestion,
        };
        longDecorations.push(decorations);
    } else {
        console.log("in unuseddd");
        // If tag is 'unused', handle the unused variable decoration
        const decorations = {
            range: new vscode.Range(line - 1, 0, line - 1, 100),
            hoverMessage: suggestion,
        };
        unusedDecorations.push(decorations);
    }
});
    const allDecorations = [...longDecorations, ...unusedDecorations];
    editor.setDecorations(decorationType, allDecorations);
}

// Command to trigger file and folder sending and processing
function activate(context) {
    console.log('Congratulations, your extension "hackumass" is now active!');
    let disposable = vscode.commands.registerCommand('hackumass.helloWorld', sendFileAndFolderToBackend);
    context.subscriptions.push(disposable);

    vscode.workspace.onDidSaveTextDocument((document) => {
        if (document === vscode.window.activeTextEditor.document) {
            resetDecorations();  // Clear current decorations
            sendFileAndFolderToBackend();  // Reapply decorations by re-sending data
        }
    });

    vscode.workspace.onDidChangeTextDocument((event) => {
        if (event.document === vscode.window.activeTextEditor.document) {
            resetDecorations();  // Clear current decorations
            // sendFileAndFolderToBackend();  // Optionally reapply decorations by re-sending data
        }
    });
    
}

// Function to clear decorations
function resetDecorations() {
    const editor = vscode.window.activeTextEditor;
    if (editor) {
        editor.setDecorations(decorationType, []);
        console.log("All decorations reset.");
    }
}

// Deactivate function (if needed for other cleanup)
function deactivate() {
    resetDecorations();
    console.log("Extension deactivated.");
}

module.exports = {
    activate,
    deactivate
};
