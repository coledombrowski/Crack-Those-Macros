import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';


const DailyMacros = () => {
    const value = 50;
    return (
        <div>
        <div>
          Breakfest{value} / 100
        </div>
        <div style={{ width: '100px', height: '100px' }}>
          <CircularProgressbar
            value={value}
            text={`${value}/Total`}
            styles={buildStyles({
              textSize: '16px',
              pathColor: `rgba(62, 152, 199, ${value / 100})`,
              textColor: '#f88',
              trailColor: '#d6d6d6',
              backgroundColor: '#3e98c7',
            })}
          />
        </div>
        <div>
          Lunch{value} / 100
        </div>
        <div style={{ width: '100px', height: '100px' }}>
          <CircularProgressbar
            value={70}
            text={`${70}%`}
            styles={buildStyles({
              textSize: '16px',
              pathColor: `rgba(62, 152, 199, ${70 / 100})`,
              textColor: '#f88',
              trailColor: '#d6d6d6',
              backgroundColor: '#3e98c7',
            })}
          />
        </div>
        <div>
          Dinner {value} / 100
        </div>
        <div style={{ width: '100px', height: '100px' }}>
          <CircularProgressbar
            value={value}
            text={`${value}%`}
            styles={buildStyles({
              textSize: '16px',
              pathColor: `rgba(62, 152, 199, ${value / 100})`,
              textColor: '#f88',
              trailColor: '#d6d6d6',
              backgroundColor: '#3e98c7',
            })}
          />
        </div>
        <div>
          Total {value} / 100
        </div>
        <div style={{ width: '100px', height: '100px' }}>
          <CircularProgressbar
            value={value}
            text={`${value}%`}
            styles={buildStyles({
              textSize: '16px',
              pathColor: `rgba(62, 152, 199, ${value / 100})`,
              textColor: '#f88',
              trailColor: '#d6d6d6',
              backgroundColor: '#3e98c7',
            })}
          />
        </div>
        </div>
      );
    };

export default DailyMacros;
