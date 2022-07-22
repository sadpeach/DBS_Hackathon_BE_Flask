import * as React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';

export default function WalletAccordion({walletName,walletData}) {
  return (
    <div>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography>{walletName}</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            {walletData}
          </Typography>

          <br></br>
          <Button variant="contained">REMOVE WALLET</Button>
        </AccordionDetails>
      </Accordion>
    </div>
  );
}
