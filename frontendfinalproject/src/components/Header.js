import React from 'react'
import {
    AppBar,
    Container,
    MenuItem,
    Select,
    Toolbar,
    Typography,
  } from "@material-ui/core";
  import {
    createTheme,
    makeStyles,
    ThemeProvider,
  } from "@material-ui/core/styles";
//   import { useHistory } from "react-router-dom"

import { CryptoState } from "../CryptoContext";
import { useNavigate } from 'react-router-dom';



const useStyles = makeStyles((theme) => ({
  title: {
    flex: 1,
    color: "Gold",
      fontFamily: "Montserrat",
      fontWeight: "bold",
      cursor: "pointer",
    },
  }));

  const darkTheme = createTheme({
    palette: {
      primary: {
        main: "#fff",
      },
      type: "dark",
    },
  })
  
  
  const Header = () => {
    const navigate = useNavigate();
    const classes = useStyles();
    const { currency, setCurrency } = CryptoState();
    
    
    // const history = useHistory();

  return (
    <ThemeProvider theme={darkTheme}>
    <AppBar color="transparent" position="static">
      <Container>
        <Toolbar>
          <Typography
            onClick={() => navigate(`/`)}
            variant="h6"
            className={classes.title}
          >
            Cryptosy
          </Typography>
          {/* <Button color="inherit">Login</Button> */}
          <Select
            variant="outlined"
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={currency}
            style={{ width: 100, height: 40, marginLeft: 15 }}
            onChange={(e) => setCurrency(e.target.value)}
          >
            <MenuItem value={"USD"}>USD</MenuItem>
            <MenuItem value={"INR"}>INR</MenuItem>
          </Select>
        </Toolbar>
      </Container>
    </AppBar>
  </ThemeProvider>
  )
}

export default Header