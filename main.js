async function main() {
    // 初始化 Pyodide
    let pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/",
    });

    // 绑定分析按钮
    document.getElementById("analyzeButton").addEventListener("click", async () => {
        try {
            // 获取用户输入
            const userInput = document.getElementById("userInput").value;

            // 加载 CSV 文件
            const csvResponse = await fetch("data.csv");
            const csvData = await csvResponse.text();

            // 加载 Python 文件
            const pyResponse = await fetch("analysis.py");
            const pyCode = await pyResponse.text();

            // 将用户输入和 CSV 数据传递给 Python
            pyodide.globals.set("userInput", userInput);
            pyodide.globals.set("csvData", csvData);

            // 运行 Python 代码
            await pyodide.runPythonAsync(pyCode);

            // 调用 Python 函数
            const analyze_csv = pyodide.globals.get("analyze_csv");
            const output = analyze_csv();

            // 将多行文本转换为 HTML 格式
            const formattedOutput = output.replace(/\n/g, "<br>");

            // 将结果输出到页面
            document.getElementById("output").innerHTML = formattedOutput;
        } catch (error) {
            console.error("Error running analysis:", error);
            document.getElementById("output").innerHTML = "An error occurred. Please check the console.";
        }
    });
}

// 启动 Pyodide 运行时
main();