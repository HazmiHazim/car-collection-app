import { FC } from "react";
import MainLayout from "../layout/mainLayout";
import { Button, Grid } from "@mui/material";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import AddIcon from "@mui/icons-material/Add";

function createData(
  name: string,
  brand: string,
  model: string,
  category: string,
  description: string,
  image: string
) {
  return { name, brand, model, category, description, image };
}

const rows = [
  createData(
    "Saga",
    "Proton",
    "v2",
    "Sedan",
    "Kereta keluaran pertama Malaysia",
    "/images/cars/saga.png"
  ),
  createData(
    "Saga",
    "Proton",
    "v2",
    "Sedan",
    "Kereta keluaran pertama Malaysia",
    "/images/cars/saga.png"
  ),
  createData(
    "Saga",
    "Proton",
    "v2",
    "Sedan",
    "Kereta keluaran pertama Malaysia",
    "/images/cars/saga.png"
  ),
  createData(
    "Saga",
    "Proton",
    "v2",
    "Sedan",
    "Kereta keluaran pertama Malaysia",
    "/images/cars/saga.png"
  ),
];

const Car: FC = () => {
  return (
    <MainLayout>
      <Grid
        xs
        item
        md={12}
        sx={{ display: "flex", justifyContent: "flex-end" }}
      >
        <Button variant="contained" disableElevation startIcon={<AddIcon />}>
          Create new car
        </Button>
      </Grid>
      <Grid xs item md={12}>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Car Name</TableCell>
                <TableCell align="right">Brand</TableCell>
                <TableCell align="right">Model</TableCell>
                <TableCell align="right">Category</TableCell>
                <TableCell align="right">Description</TableCell>
                <TableCell align="right">Image</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.name}
                  </TableCell>
                  <TableCell align="right">{row.brand}</TableCell>
                  <TableCell align="right">{row.model}</TableCell>
                  <TableCell align="right">{row.category}</TableCell>
                  <TableCell align="right">{row.description}</TableCell>
                  <TableCell align="right">{row.image}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </MainLayout>
  );
};

export default Car;
