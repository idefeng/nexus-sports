import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Stats } from './pages/Stats';
import { Explorer } from './pages/Explorer';
import { Import } from './pages/Import';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/explorer" element={<Explorer />} />
          <Route path="/import" element={<Import />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
