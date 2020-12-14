import React from "react";

function App() {
  const sayHello = () => {
    console.log("hello");
  }

  return (
    <div>
      <h2>Insert a startup or project idea that you have, and we'll try to predict</h2>
      <button onClick = {sayHello}>Hello</button>
    </div>

  );
}

export default App;

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
