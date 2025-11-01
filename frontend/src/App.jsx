import { useState } from "react";

function App() {
    const [message, setMessage] = useState("");
    const [predictions, setPredictions] = useState([]);

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:8000/upload", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();
            setPredictions(result.questions || []);
            setMessage("✅ Dosya başarıyla analiz edildi!");
        } catch (error) {
            setMessage("❌ Dosya yükleme başarısız.");
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>📘 Sınav Tahmin AI</h1>
            <p>Ders slaytını yükle, sistem muhtemel sınav sorularını tahmin etsin.</p>

            <input type="file" onChange={handleFileUpload} />
            <p>{message}</p>

            {predictions.length > 0 && (
                <div>
                    <h3>Tahmin Edilen Sorular:</h3>
                    <ul>
                        {predictions.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;
