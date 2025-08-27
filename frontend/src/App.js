import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
    const [text, setText] = useState('');
    const [mode, setMode] = useState('summarize'); // 'summarize' or 'proofread'
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);
        setError('');

        try {
            const response = await axios.post(`${API_BASE_URL}/${mode}`, { text });
            setResult(response.data);
        } catch (err) {
            setError('エラーが発生しました。APIサーバーが起動しているか確認してください。');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const renderResult = () => {
        if (loading) {
            return (
                <div className="d-flex justify-content-center align-items-center h-100">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            );
        }

        if (error) {
            return <div className="alert alert-danger">{error}</div>;
        }

        if (!result) {
            return <p className="text-muted">ここに結果が表示されます。</p>;
        }

        if (mode === 'summarize') {
            return <p>{result.summary}</p>;
        }

        if (mode === 'proofread' && result.corrections) {
            return (
                <div className="table-responsive">
                    <table className="table table-bordered table-hover">
                        <thead className="table-light">
                            <tr>
                                <th scope="col">修正前</th>
                                <th scope="col">修正後</th>
                                <th scope="col">理由</th>
                            </tr>
                        </thead>
                        <tbody>
                            {result.corrections.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.original}</td>
                                    <td>{item.corrected}</td>
                                    <td>{item.reason}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            );
        }

        return null;
    };

    return (
        <div className="container py-5">
            <header className="text-center mb-5">
                <h1 className="display-4">AIライティング支援ツール</h1>
                <p className="lead text-muted">文章の要約と校正をサポートします</p>
            </header>

            <div className="row">
                <div className="col-lg-6 mb-4 mb-lg-0">
                    <div className="card h-100">
                        <div className="card-body">
                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <div className="btn-group w-100" role="group">
                                        <input type="radio" className="btn-check" name="mode" id="summarize" autoComplete="off" checked={mode === 'summarize'} onChange={() => setMode('summarize')} />
                                        <label className="btn btn-outline-primary" htmlFor="summarize">要約</label>

                                        <input type="radio" className="btn-check" name="mode" id="proofread" autoComplete="off" checked={mode === 'proofread'} onChange={() => setMode('proofread')} />
                                        <label className="btn btn-outline-primary" htmlFor="proofread">校正</label>
                                    </div>
                                </div>
                                <div className="mb-3">
                                    <textarea
                                        className="form-control"
                                        rows="15"
                                        value={text}
                                        onChange={(e) => setText(e.target.value)}
                                        placeholder={mode === 'summarize' ? 'ここに要約したい文章を入力してください...' : 'ここに校正したい文章を入力してください...'}
                                        required
                                    />
                                </div>
                                <div className="d-grid">
                                    <button type="submit" className="btn btn-primary btn-lg" disabled={loading || !text.trim()}>
                                        {loading ? '処理中...' : '実行'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <div className="col-lg-6">
                    <div className="card h-100 result-card">
                        <div className="card-body">
                            <h5 className="card-title mb-3">結果</h5>
                            {renderResult()}
                        </div>
                    </div>
                </div>
            </div>

            <footer className="text-center text-muted mt-5">
                <p>&copy; 2024 AI Writing Assistant</p>
            </footer>
        </div>
    );
}

export default App;