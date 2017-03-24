import React from 'react';
import { Route, IndexRoute } from 'react-router';

import { MainPage }  from "pages/MainPage.jsx";
import { PageFrame } from "pages/PageFrame.jsx";

export var routes = (
    <Route path="/" component={ PageFrame }>
        <IndexRoute component={ MainPage }/>
    </Route>
)
