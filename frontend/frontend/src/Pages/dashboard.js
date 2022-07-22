import { Link } from "react-router-dom";
import WalletAccordion from "../Components/walletAccordion";
import { useEffect, useState } from "react";
import axios from 'axios';
import TransactionForm from "../Components/transactionForm";

export default function Dashboard() {

  const [wallets, setWallet] = useState([]);
  const [currencies, setCurrentcies] = useState([]);

  //TODO: axios call for backend data
  useEffect(() => {
    // Update the document title using the browser API
    // get all wallet's data
    // const url = "";
    // var allWallet = await axios.get(url);

    var allWallet = {
      data: [
        {
          id: 1,
          name: "wallet1",
          data: "wallet1data"
        },
        {
          id: 2,
          name: "wallet2",
          data: "wallet2data"
        },
        {
          id: 3,
          name: "wallet3",
          data: "wallet3data"
        }
      ]
    };

    var allCurrencies = {
      data: [
        {
          id: 1,
          name: "currency1",
          data: "35.3"
        },
        {
          id: 2,
          name: "currency2",
          data: "38.3"
        },
        {
          id: 3,
          name: "currency3",
          data: "59.3"
        },
      ]
    };

    setWallet(allWallet.data);
    setCurrentcies(allCurrencies.data);
  }, []);

  return (
    <>

      {/* accordion */}
      {
        wallets.map(wallet => {
          return <WalletAccordion key={'wallet_id' + wallet.id} walletName={wallet.name} walletData={wallet.data}></WalletAccordion>
        })
      }

      <br></br>
      {/* create transaction */}
      <h3 color= 'black'>CREATE TRANSACTION</h3>
      <br></br>
      <br></br>
      <br></br>
      <TransactionForm wallets={wallets} currencies={currencies}></TransactionForm>

    </>
  );
}