// js僅負責初始化pyodide及python腳本加載
async function main() {
    // 提示開始
    var output = document.getElementById("txt_output");
    output.innerHTML = "正在初始化……";
    // 初始化 Pyodide
    let pyodide = await loadPyodide({
        indexURL: "pyodide/",
    });
    // 實際的import
    pyodide.runPythonAsync( await (await fetch("pyodide_tools.py")).text() );
    pyodide.runPythonAsync( await (await fetch("analysis.py")).text() );
    // 業務邏輯
    pyodide.runPythonAsync( await (await fetch("main.py")).text() );
    // 提示結束
    output.innerHTML = "初始化完成"
}
main();