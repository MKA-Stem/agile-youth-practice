import React from 'react';
import { Route, IndexRoute } from 'react-router';

import { MainPage }  from "pages/mainPage.jsx";
import { PageFrame } from "pages/pageFrame.jsx";

export var routes = (
    <Route path="/" component={ PageFrame }>
        <IndexRoute component={ MainPage }/>
    </Route>
)
