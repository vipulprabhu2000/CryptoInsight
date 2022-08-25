import React from 'react'
import { Container, makeStyles, Typography } from "@material-ui/core";
import Carousel from "./Carousel";
import cryptosy from './img/Cryotosy1.png'

const useStyles = makeStyles((theme) => ({
    banner: {
      backgroundImage: "url(public/banner2.jpg)",
    },
    bannerContent: {
      height: 400,
      display: "flex",
      flexDirection: "column",
      paddingTop: 10,
      justifyContent: "space-around",
    },
    tagline: {
      display: "flex",
      height: "40%",
      flexDirection: "column",
      justifyContent: "center",
      textAlign: "center",
    },
    carousel: {
      height: "50%",
      display: "flex",
      alignItems: "center",
    },
    
  }));

const Banner = () => {
   const classes = useStyles();

  return (
    <div className={classes.banner}>
    <Container className={classes.bannerContent}>
      <div className={classes.tagline}>
        {/* <Typography
          variant="h2"
          style={{
            fontWeight: "bold",
            marginBottom: 15,
            fontFamily: "Montserrat",
          }}
        >
          Cryptosy
        </Typography> */}
        <img src={cryptosy} alt='Cryotosy' style={{
          width:"350px",
          margin:"auto",
          borderBottom: "1px solid white"
          
        }} />
        {/* <hr/> */}

        {/* <Typography
          variant="subtitle2"
          style={{
            color: "darkgrey",
            textTransform: "capitalize",
            fontFamily: "Montserrat",
          }}
        >
          Get all the Info regarding your favorite Crypto Currency
        </Typography> */}
      </div>
      <Carousel />
    </Container>
  </div>
  )
}

export default Banner