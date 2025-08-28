import React, { useState } from 'react';
import axios from 'axios';
import {
    AppBar,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Container,
    CssBaseline,
    Grid,
    IconButton,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    ThemeProvider,
    ToggleButton,
    ToggleButtonGroup,
    Toolbar,
    Typography,
    createTheme
} from '@mui/material';
import { AutoFixHigh, GitHub } from '@mui/icons-material';

const API_BASE_URL = 'http://localhost:8000';

// ダークテーマの定義
const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    },
});

function App() {
    const [text, setText] = useState('');
    const [mode, setMode] = useState('summarize'); // 'summarize' or 'proofread'
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleModeChange = (event, newMode) => {
        if (newMode !== null) {
            setMode(newMode);
        }
    };

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
                <Grid container justifyContent="center" alignItems="center" sx={{ height: '100%' }}>
                    <CircularProgress />
                </Grid>
            );
        }

        if (error) {
            return <Typography color="error">{error}</Typography>;
        }

        if (!result) {
            return <Typography variant="body2" color="text.secondary">ここに結果が表示されます。</Typography>;
        }

        if (mode === 'summarize') {
            return <Typography variant="body1">{result.summary}</Typography>;
        }

        if (mode === 'proofread' && result.corrections) {
            if (result.corrections.length === 0) {
                return <Typography variant="body1">修正点は見つかりませんでした。</Typography>;
            }
            return (
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>修正前</TableCell>
                                <TableCell>修正後</TableCell>
                                <TableCell>理由</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {result.corrections.map((item, index) => (
                                <TableRow key={index}>
                                    <TableCell component="th" scope="row">{item.original}</TableCell>
                                    <TableCell>{item.corrected}</TableCell>
                                    <TableCell>{item.reason}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            );
        }

        return null;
    };

    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <AppBar position="static">
                <Toolbar>
                    <AutoFixHigh sx={{ mr: 2 }} />
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        AIライティング支援ツール
                    </Typography>
                    <IconButton color="inherit" href="https://github.com/your-github/ai_writer_project" target="_blank">
                        <GitHub />
                    </IconButton>
                </Toolbar>
            </AppBar>
            <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
                <Grid container spacing={4}>
                    {/* 左側の入力エリア */}
                    <Grid item xs={12} md={6}>
                        <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
                            <Typography variant="h5" gutterBottom>テキスト入力</Typography>
                            <form onSubmit={handleSubmit}>
                                <ToggleButtonGroup
                                    color="primary"
                                    value={mode}
                                    exclusive
                                    onChange={handleModeChange}
                                    fullWidth
                                    sx={{ mb: 2 }}
                                >
                                    <ToggleButton value="summarize">要約</ToggleButton>
                                    <ToggleButton value="proofread">校正</ToggleButton>
                                </ToggleButtonGroup>
                                <TextField
                                    multiline
                                    rows={15}
                                    fullWidth
                                    variant="outlined"
                                    value={text}
                                    onChange={(e) => setText(e.target.value)}
                                    placeholder={mode === 'summarize' ? 'ここに要約したい文章を入力してください...' : 'ここに校正したい文章を入力してください...'}
                                    required
                                    sx={{ mb: 2 }}
                                />
                                <Button
                                    type="submit"
                                    variant="contained"
                                    size="large"
                                    fullWidth
                                    disabled={loading || !text.trim()}
                                    startIcon={loading ? <CircularProgress size={24} color="inherit" /> : <AutoFixHigh />}
                                >
                                    {loading ? '処理中...' : '実行'}
                                </Button>
                            </form>
                        </Paper>
                    </Grid>

                    {/* 右側の結果エリア */}
                    <Grid item xs={12} md={6}>
                        <Paper elevation={3} sx={{ p: 3, height: '100%', minHeight: '400px' }}>
                            <Typography variant="h5" gutterBottom>結果</Typography>
                            {renderResult()}
                        </Paper>
                    </Grid>
                </Grid>
            </Container>
        </ThemeProvider>
    );
}

export default App;
