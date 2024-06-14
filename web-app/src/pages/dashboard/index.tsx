import { FC } from "react";
import MainLayout from "../layout/mainLayout";
import { Grid, Paper, Typography } from "@mui/material";

const Dashboard: FC = () => {
  return (
    <MainLayout>
      <Grid xs item md={12}>
        <Typography variant="h6" color="#A9A9A9" noWrap sx={{ flexGrow: 1 }}>
          Dashboard
        </Typography>
      </Grid>
      <Grid xs item md={6}>
        <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
          Test
        </Paper>
      </Grid>
      <Grid xs item md={6}>
        <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
          Test
        </Paper>
      </Grid>
      <Grid xs item md={12}>
        <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
          Test
        </Paper>
      </Grid>
      <Grid xs item md={12}>
        <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
          Test
        </Paper>
      </Grid>
    </MainLayout>
  );
};

export default Dashboard;
