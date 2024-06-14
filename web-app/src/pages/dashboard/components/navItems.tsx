import { Fragment } from "react";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import ListSubheader from "@mui/material/ListSubheader";
import AssignmentIcon from "@mui/icons-material/Assignment";
import SpaceDashboardIcon from "@mui/icons-material/SpaceDashboard";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";
import CategoryIcon from "@mui/icons-material/Category";
import StarsIcon from "@mui/icons-material/Stars";
import ColorLensIcon from "@mui/icons-material/ColorLens";
import { useRouter } from "next/navigation";

export const mainListItems = (
  <Fragment>
    <ListItemButton>
      <ListItemIcon>
        <SpaceDashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <DirectionsCarIcon />
      </ListItemIcon>
      <ListItemText primary="Cars" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <StarsIcon />
      </ListItemIcon>
      <ListItemText primary="Brands" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <CategoryIcon />
      </ListItemIcon>
      <ListItemText primary="Categories" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <ColorLensIcon />
      </ListItemIcon>
      <ListItemText primary="Colours" />
    </ListItemButton>
  </Fragment>
);

export const secondaryListItems = (
  <Fragment>
    <ListSubheader component="div" inset>
      Saved reports
    </ListSubheader>
    <ListItemButton>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Current month" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Last quarter" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Year-end sale" />
    </ListItemButton>
  </Fragment>
);
