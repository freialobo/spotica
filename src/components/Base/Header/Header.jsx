import React from 'react';
import { Link } from 'react-router';

import Icon from '../../Icon/Icon';
import Button from '../../Button/Button';

import './style.scss';

const Header = React.createClass({
  generateLogin() {
    return (
      <Button
        className="header__signin"
        color="camoflauge"
        compact>
        Connect Spotify
      </Button>
    );
  },

  render() {
    return (
      <header className="header">
        <div className="header__container">
          <Link to='/'>
            <span className="logo">
              <Icon className="logo__icon">music_note</Icon>
              <h1 className="logo__title">Spotica</h1>
            </span>
          </Link>

          <span>
            <Icon className="header__icon">equalizer</Icon>
            <Icon className="header__icon">settings</Icon>
            <Icon className="header__icon">person</Icon>
          </span>
        </div>
      </header>
    );
  }
});

export default Header;
