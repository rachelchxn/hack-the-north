import React from 'react'
import styled from '@emotion/styled'
import { keyframes } from '@emotion/react';
import { useNavigate } from 'react-router-dom';
import video from '../../res/glasses.mp4';

const Header = () => {
  const nav = useNavigate();
  return (
    <HeaderContainer>
      <video autoPlay loop muted playsinline>
          <source src={video} type='video/mp4' />
      </video>
      <TextContainer>
        <h1>Meet Visionary, the <span>Apple</span> of your <span>Eye</span>.</h1>
        <p>Correct harmful eye habits before its too late with the Visionary glasses and built-in app.</p>
        <button onClick={() => nav('./dashboard')}>Get Started</button>
      </TextContainer>

    </HeaderContainer>
  )
}

const HeaderContainer = styled.div`
  width: 100vw;
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  position: relative;
  justify-content: center;
  > video {
    position: absolute;
    right: 55px;
    width: 500px;
    z-index: 0;
  }

  @media (max-width: 75em) {
    > video {
      display: none;
    }
  }
`


const TextContainer = styled.div`
  width: 48vw;
  margin-left: 15vw;
  z-index: 10;
  display: flex;
  flex-direction: column;
  font-family: Helvetica Now Display;
  > h1 {
    line-height: 1.4;
    font-size: 54px;
    margin-bottom: 2px;
    font-weight: 700;
    > span {
      background-image: linear-gradient(to bottom right, #FCA27C, #FF5AB4);
      background-size: 100%;
      -webkit-background-clip: text;
      -moz-background-clip: text;
      -webkit-text-fill-color: transparent; 
      -moz-text-fill-color: transparent;
    }
  }
  > p {
    font-size: 22px;
    margin-bottom: 60px;
  }
  > button {
    border: none;
    background-color: #222222;
    border-radius: 6px;
    color: white;
    width: 220px;
    padding: 16px;
    font-size: 18px;
    padding-left: 47px;
    padding-right: 47px;
    cursor: pointer;
    transition: background 0.5s;
    background: linear-gradient(90deg, var(--c1, #f6d365), var(--c2, #fda085) 51%, var(--c1, #f6d365)) var(--x, 0)/ 200%;
    --c1: #FCA27C;
    --c2: #FF5AB4;
    :hover {
      --x: 100%;
    }
    
    
  }

`
export default Header
