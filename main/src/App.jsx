import "./App.css";     

import { Container, InputGroup, FormControl, Button } from "react-bootstrap";
const clientId = import.meta.SPOTIFY_CLIENT_ID;
const clientSecret = import.meta.SPOTIFY_CLIENT_SECRET;

function App() {
  return (
<Container>
  <InputGroup>
    <FormControl
      placeholder="Search For Artist"
      type="input"
      aria-label="Search for an Artist"
      style={{
        width: "300px",
        height: "35px",
        borderWidth: "0px",
        borderStyle: "solid",
        borderRadius: "5px",
        marginRight: "10px",
        paddingLeft: "10px",
      }}
    />
    <Button onClick={() => {}}>Search</Button>
    <Button onClick={{}}>Search</Button>
  </InputGroup>
</Container>
  );
}
export default App;