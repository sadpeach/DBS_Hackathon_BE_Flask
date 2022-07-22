import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Container from '@mui/material/Container';
import { useEffect, useState } from "react";
import axios from 'axios';
import { Button } from '@mui/material';

export default function TransactionForm({wallets, currencies}) {

    console.log("currencies:"+currencies);

    const [selectedWalletId, setSelectedWalletId] = useState(0);
    const [selectedCurrencyId, setCurrencyId] = useState(0);

    const handleWalletChange = (event) => {
        setSelectedWalletId(event.target.value);
      };

    const handleCurrencyChange = (event) => {
        selectedCurrencyId(event.target.value);
    };

    return (
        <Container>
        <div>
            <form>
                <TextField 
                    id="amount"
                    label="Amount"
                    type="text">
                </TextField>

                <br></br>
                <br></br>

                <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Select Wallet</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        label="selectWallet"
                        onChange={handleWalletChange}
                    >
                        {wallets.map(wallet => {
                            return <MenuItem value={wallet.id}>{wallet.name}</MenuItem>})}
                    </Select>
                </FormControl>

                <br></br>
                <br></br>

                <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Select Currency</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        label="selectcurrency"
                        onChange={handleCurrencyChange}
                    >
                        {currencies.map(currency => {
                            return <MenuItem value={currency.id}>{currency.name}</MenuItem>})}
                    </Select>
                </FormControl>

                <Button variant="contained">Top Up</Button>
                <br></br>
                <Button variant="contained">Transfer</Button>

            </form>
        </div>
        </Container>
    );
}
