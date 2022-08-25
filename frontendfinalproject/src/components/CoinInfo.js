import axios from "axios";
import { useEffect, useState } from "react";
import { HistoricalChart } from "../config/api";
import { Line } from "react-chartjs-2";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  CategoryScale,
 
} from "chart.js";
import { Doughnut } from "react-chartjs-2";

import {
  Box,
  CircularProgress,
  createTheme,
  makeStyles,
  ThemeProvider,
} from "@material-ui/core";
import SelectButton from "./SelectButton";
/* import { chartDays } from "../config/data"; */
import { CryptoState } from "../CryptoContext";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
);

const CoinInfo = ({ coin }) => {
  const [historicData, setHistoricData] = useState();
 /*  const [days, setDays] = useState(1); */
  const { currency } = CryptoState();
  const [flag, setflag] = useState(false);
  const [coins, setCoins] = useState([]);
 /*  const [dataml, setdataml] = useState([]);
  const [loading, setLoading] = useState(false); */

 
const x=[];
const y=[];



  const useStyles = makeStyles((theme) => ({
    container: {
      width: "75%",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      marginTop: 25,
      padding: 40,
      [theme.breakpoints.down("md")]: {
        width: "100%",
        marginTop: 0,
        padding: 20,
        paddingTop: 0,
      },
    },
    small_container:{
      width:"auto",
      padding:"10px",
      margin:"15px",
    },
    min_container:{
      display:"block",
      width:"auto",
      margin:"auto"
    },
  }));

  const classes = useStyles();

  const fetchHistoricData = async () => {
    const { data } = await axios.get(HistoricalChart(coin.id, 1, currency));
    setflag(true);
    setHistoricData(data.prices);
  };

  useEffect(() => {
    fetchHistoricData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const darkTheme = createTheme({
    palette: {
      primary: {
        main: "#fff",
      },
      type: "dark",
    },
  });
  const api1 = axios.create({
    baseURL: "https://cryptosyapi.herokuapp.com/SentimentAnalyzer/",
  });
  const api2 = axios.create({
    baseURL: "https://cryptosyapi.herokuapp.com/TechnicalAnalysis/",
  });

  const createcourse = async () => {
    try {
      let coin_data = await api1.post("/", { h: coin.id });

      setCoins([
        coin_data.data.Positive,
        coin_data.data.Negative,
        coin_data.data.Neutral,
        coin_data.data.Subjectivity,
      ]);
    } catch (error) {
      console.log(error);
    }
  };
  const createcourse1 = async () => {
    try {
      let coin_state = await api2.post("/", { h: coin.id });

    


      for (let i = 0; i < 50; i++) {
        let j=parseInt(i);
        let m=parseFloat(coin_state.data[i].magnitude);
        y.push(j);
        x.push(m);
        m=0;
      }
   
    } catch (error) {
      console.log(error);
    }
  }

  var data = {
    labels: ["Positive", "Negative", "Neutral"],
    datasets: [
      {
        label: "# of Votes",
        data: [coins[0], coins[1], coins[2]],
        backgroundColor: [
          "rgba(255, 99, 132)",
          "rgba(54, 162, 235)",
          "rgba(255, 206, 86)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
        ],
        borderWidth: 1,
        
      },
    ],
  };
  useEffect(() => {
    createcourse1()
    
    
  },);

 const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Line Chart',
      },
    },
  };
  const labels= y;
  const final_data = {
    labels,
    datasets: [
      {
        label: "Momentum",
        data: x,
        borderColor: "rgb(255, 255, 255)",
        backgroundColor: "rgba(255, 255,255,0.5)",
      },
    ],
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <div className={classes.container}>
        {!historicData | (flag === false) ? (
          <CircularProgress
            style={{ color: "gold" }}
            size={250}
            thickness={1}
          />
        ) : (
          <>
         
            
            <div style={{width:"60%",height:"auto"}} >
            <Line options={options} data={final_data} />
            </div>
            <div
              style={{
                display: "flex",
                marginTop: 20,
                justifyContent: "space-around",
                width: "100%",
              }}
            >
            
              <SelectButton className={classes.min_container} onClick={createcourse}>Sentiments</SelectButton>
            
            </div>
          </>
        )}
      
        <div className="sent_class" style={{display:"flex",flexDirection:"row",justifyContent:"space-evenly" ,width:"auto"}}>
        <div className={classes.small_container}>
        Positive:{coins[0]}
        </div>
        <div className={classes.small_container}>
        Negative: {coins[1]}
        </div>
        <div className={classes.small_container}>
        Neutral: {coins[2]}
        </div>
        <div className={classes.small_container}>
        Subjectivity: {coins[3]}
        </div>
        
      
        </div>
        
      
        <Box component="div" m={1} >
          <Doughnut data={data}  width={400} height={200} options={{
          responsive: true,
          maintainAspectRatio: true,
        }}/>
        </Box>
      </div>
    </ThemeProvider>
  );
};



export default CoinInfo;
