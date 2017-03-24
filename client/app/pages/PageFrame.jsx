import React from 'react';
import Helmet from "react-helmet";
import { Link } from 'react-router';

import "pages/PageFrame.scss";

var DEV = process.env.NODE_ENV != "production";

export var PageFrame = (props) => (
	<div>
		<Helmet
			titleTemplate="%s - STEM"
			defaultTitle="STEM"
			link={DEV?[]:[ // if it's dev, styles are in js.
				{"rel":"stylesheet", "href": "/style.css"}
			]}
			meta={[
				{"name":"viewport", "content":"width=device-width, initial-scale=1"}
			]}
		/>
		<div className="container">
			<h1>This is the page frame</h1>
			{props.children}
		</div>
	</div>
);
