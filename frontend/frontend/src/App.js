import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './Pages/dashboard';
import Login from './LoginPage/login.js';

function App() {
  return (
    <div className="App">
        <Router>
          <Routes>
            <Route path="/dashboard" element={<Dashboard/>}></Route>
            <Route path="/login" element={<Login/>} ></Route>
          </Routes>
        </Router>
    </div>
  );
}

export default App;
