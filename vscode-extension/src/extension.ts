import * as vscode from 'vscode';
import * as path from 'path';
import { exec } from 'child_process';
import { promises as fs } from 'fs';

export function activate(context: vscode.ExtensionContext) {
    console.log('Setwise Quiz Generator extension is now active!');

    // Create webview provider for PDF preview
    const provider = new SetwisePreviewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(SetwisePreviewProvider.viewType, provider)
    );

    // Register commands
    registerCommands(context);

    // Auto-validate on save if enabled
    vscode.workspace.onDidSaveTextDocument((document) => {
        const config = vscode.workspace.getConfiguration('setwise');
        if (config.get('autoValidate') && isSetwiseQuestionsFile(document.fileName)) {
            validateQuestionsCommand(document.fileName);
        }
    });

    // Auto-preview on open if enabled
    vscode.window.onDidChangeActiveTextEditor((editor) => {
        const config = vscode.workspace.getConfiguration('setwise');
        if (config.get('autoPreview') && editor && isSetwiseQuestionsFile(editor.document.fileName)) {
            previewQuizCommand(editor.document.fileName);
        }
    });
}

function registerCommands(context: vscode.ExtensionContext) {
    // Preview Quiz command
    const previewDisposable = vscode.commands.registerCommand('setwise.previewQuiz', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || !isSetwiseQuestionsFile(editor.document.fileName)) {
            vscode.window.showErrorMessage('Please open a Setwise questions file (e.g., *questions.py)');
            return;
        }

        await previewQuizCommand(editor.document.fileName);
    });

    // Generate Quiz command
    const generateDisposable = vscode.commands.registerCommand('setwise.generateQuiz', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || !isSetwiseQuestionsFile(editor.document.fileName)) {
            vscode.window.showErrorMessage('Please open a Setwise questions file');
            return;
        }

        await generateQuizCommand(editor.document.fileName);
    });

    // Validate Questions command
    const validateDisposable = vscode.commands.registerCommand('setwise.validateQuestions', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || !isSetwiseQuestionsFile(editor.document.fileName)) {
            vscode.window.showErrorMessage('Please open a Setwise questions file');
            return;
        }

        await validateQuestionsCommand(editor.document.fileName);
    });

    // Fix LaTeX command
    const fixLatexDisposable = vscode.commands.registerCommand('setwise.fixLatex', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || !isSetwiseQuestionsFile(editor.document.fileName)) {
            vscode.window.showErrorMessage('Please open a Setwise questions file');
            return;
        }

        await fixLatexCommand(editor.document.fileName);
    });

    // Insert MCQ template
    const insertMCQDisposable = vscode.commands.registerCommand('setwise.insertMCQ', () => {
        insertTemplate('mcq');
    });

    // Insert Subjective template
    const insertSubjectiveDisposable = vscode.commands.registerCommand('setwise.insertSubjective', () => {
        insertTemplate('subjective');
    });

    // Show statistics
    const showStatsDisposable = vscode.commands.registerCommand('setwise.showStats', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || !isSetwiseQuestionsFile(editor.document.fileName)) {
            vscode.window.showErrorMessage('Please open a Setwise questions file');
            return;
        }

        await showStatsCommand(editor.document.fileName);
    });

    context.subscriptions.push(
        previewDisposable,
        generateDisposable, 
        validateDisposable,
        fixLatexDisposable,
        insertMCQDisposable,
        insertSubjectiveDisposable,
        showStatsDisposable
    );
}

function isSetwiseQuestionsFile(fileName: string): boolean {
    return fileName.includes('questions') && fileName.endsWith('.py');
}

async function previewQuizCommand(filePath: string) {
    const config = vscode.workspace.getConfiguration('setwise');
    const template = config.get('defaultTemplate', 'default');
    const sets = config.get('previewSets', 1);

    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Generating quiz preview...",
        cancellable: false
    }, async (progress) => {
        return new Promise<void>((resolve, reject) => {
            const outputDir = path.join(path.dirname(filePath), '.setwise-preview');
            const command = `setwise generate --questions-file "${filePath}" --output-dir "${outputDir}" --sets ${sets} --template ${template} --seed 42`;

            exec(command, (error, stdout, stderr) => {
                if (error) {
                    vscode.window.showErrorMessage(`Preview failed: ${error.message}`);
                    reject(error);
                    return;
                }

                // Open generated PDF
                const pdfPath = path.join(outputDir, 'quiz_set_1.pdf');
                vscode.commands.executeCommand('vscode.open', vscode.Uri.file(pdfPath));
                
                vscode.window.showInformationMessage('Quiz preview generated successfully!');
                resolve();
            });
        });
    });
}

async function generateQuizCommand(filePath: string) {
    const options = await vscode.window.showQuickPick([
        { label: '1 set', description: 'Generate 1 quiz set' },
        { label: '3 sets', description: 'Generate 3 quiz sets' },
        { label: '5 sets', description: 'Generate 5 quiz sets' },
        { label: 'Custom...', description: 'Specify custom parameters' }
    ], { placeHolder: 'How many quiz sets to generate?' });

    if (!options) return;

    let command = `setwise generate --questions-file "${filePath}"`;
    
    if (options.label === 'Custom...') {
        const sets = await vscode.window.showInputBox({
            prompt: 'Number of quiz sets',
            value: '3',
            validateInput: (value) => {
                const num = parseInt(value);
                if (isNaN(num) || num < 1 || num > 10) {
                    return 'Please enter a number between 1 and 10';
                }
                return null;
            }
        });

        const template = await vscode.window.showQuickPick([
            'default', 'compact', 'minimal'
        ], { placeHolder: 'Select template' });

        if (!sets || !template) return;
        command += ` --sets ${sets} --template ${template}`;
    } else {
        const sets = options.label.split(' ')[0];
        command += ` --sets ${sets}`;
    }

    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Generating quiz...",
        cancellable: false
    }, async (progress) => {
        return new Promise<void>((resolve, reject) => {
            exec(command, { cwd: path.dirname(filePath) }, (error, stdout, stderr) => {
                if (error) {
                    vscode.window.showErrorMessage(`Generation failed: ${error.message}`);
                    reject(error);
                    return;
                }

                vscode.window.showInformationMessage('Quiz generated successfully! Check the output folder.');
                resolve();
            });
        });
    });
}

async function validateQuestionsCommand(filePath: string) {
    return new Promise<void>((resolve, reject) => {
        const command = `setwise questions validate "${filePath}"`;
        
        exec(command, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Validation failed: ${stderr || error.message}`);
                reject(error);
                return;
            }

            if (stdout.includes('Valid')) {
                vscode.window.showInformationMessage(`✅ ${stdout.trim()}`);
            } else {
                vscode.window.showWarningMessage(`⚠️ ${stdout.trim()}`);
            }
            resolve();
        });
    });
}

async function fixLatexCommand(filePath: string) {
    const choice = await vscode.window.showQuickPick([
        { label: 'Preview fixes', description: 'Show what fixes would be applied' },
        { label: 'Apply fixes', description: 'Apply fixes to the file' }
    ], { placeHolder: 'LaTeX error fixing options' });

    if (!choice) return;

    const isDryRun = choice.label === 'Preview fixes';
    const command = `setwise questions fix-latex "${filePath}"${isDryRun ? ' --dry-run' : ''}`;

    return new Promise<void>((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Fix failed: ${error.message}`);
                reject(error);
                return;
            }

            if (isDryRun) {
                vscode.window.showInformationMessage(`LaTeX fixes preview:\n${stdout}`);
            } else {
                vscode.window.showInformationMessage('LaTeX errors fixed successfully!');
                // Reload the file to show changes
                vscode.commands.executeCommand('workbench.action.files.revert');
            }
            resolve();
        });
    });
}

async function showStatsCommand(filePath: string) {
    return new Promise<void>((resolve, reject) => {
        const command = `setwise questions stats "${filePath}"`;
        
        exec(command, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`Stats failed: ${error.message}`);
                reject(error);
                return;
            }

            // Show stats in a new untitled document
            vscode.workspace.openTextDocument({
                content: stdout,
                language: 'plaintext'
            }).then(doc => {
                vscode.window.showTextDocument(doc);
            });
            resolve();
        });
    });
}

function insertTemplate(type: 'mcq' | 'subjective') {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const templates = {
        mcq: `    {
        "question": r"Your question here?",
        "options": [
            r"Option A",
            r"Option B",
            r"Option C", 
            r"Option D"
        ],
        "answer": r"Option A",
        "marks": 1
    },`,
        subjective: `    {
        "question": r"Your subjective question here.",
        "answer": r"Sample answer or solution steps.",
        "marks": 5
    },`
    };

    editor.edit(editBuilder => {
        editBuilder.insert(editor.selection.active, templates[type]);
    });
}

class SetwisePreviewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'setwise.previewView';

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Setwise Preview</title>
            <style>
                body { font-family: var(--vscode-font-family); margin: 0; padding: 20px; }
                .header { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
                .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
                .stat-card { background: var(--vscode-editor-background); border: 1px solid var(--vscode-widget-border); padding: 15px; border-radius: 6px; }
                .actions { display: flex; gap: 10px; flex-wrap: wrap; }
                .btn { background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
                .btn:hover { background: var(--vscode-button-hoverBackground); }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🎯 Setwise Quiz Generator</h2>
                <p>Professional LaTeX quiz generation in VSCode</p>
            </div>
            
            <div id="content">
                <p>Open a questions.py file to see live preview and statistics here.</p>
            </div>

            <div class="actions">
                <button class="btn" onclick="previewQuiz()">📄 Preview Quiz</button>
                <button class="btn" onclick="generateQuiz()">🚀 Generate Quiz</button>
                <button class="btn" onclick="validateQuestions()">✅ Validate</button>
                <button class="btn" onclick="fixLatex()">🔧 Fix LaTeX</button>
            </div>

            <script>
                const vscode = acquireVsCodeApi();
                
                function previewQuiz() {
                    vscode.postMessage({ command: 'previewQuiz' });
                }
                
                function generateQuiz() {
                    vscode.postMessage({ command: 'generateQuiz' });
                }
                
                function validateQuestions() {
                    vscode.postMessage({ command: 'validateQuestions' });
                }
                
                function fixLatex() {
                    vscode.postMessage({ command: 'fixLatex' });
                }
            </script>
        </body>
        </html>`;
    }
}

export function deactivate() {}