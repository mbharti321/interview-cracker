// Create a simple React functional component in TypeScript called GreetingCard that accepts a name prop (string) 
// and an optional message prop (string). The component should display 'Hello, [name]!' and if message is provided, 
// it should display it below the greeting.

import React from 'react';

type GreetingCardProps = {
  name: string;
  message?: string;
};

export const GreetingCard: React.FC<GreetingCardProps> = ({ name, message }) => {
  return (
    <div style={{ border: '1px solid #ddd', padding: 12, borderRadius: 8 }}>
      <h3>Hello, {name}!</h3>
      {message ? <p>{message}</p> : null}
    </div>
  );
};

export default GreetingCard;

// Usage example:
// <GreetingCard name="Alice" message="Welcome to the app!" />
