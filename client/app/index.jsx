import React from 'react';
import ReactDOM from 'react-dom';
import { Router, browserHistory } from 'react-router';

import {routes} from "routes.jsx";

// Client render
// Mount the react app into a DOM node.
// This is basically the entry point of the entire app.
ReactDOM.render(
	<Router history={browserHistory} routes={routes}/>, 
	document.getElementById('root')
);
