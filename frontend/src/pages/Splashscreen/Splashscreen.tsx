import { Helmet } from "react-helmet";
import { Text, Img } from "../../components"; 
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const SplashscreenPage: React.FC = () => {
  const navigate = useNavigate();
  const [distance, setDistance] = useState<number | null>(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/sensor/');
        const { distance } = response.data;
        setDistance(distance);
        if (distance <= 92) { // 1 foot = 30.48 cm
          navigate('/home'); // Adjust this path if needed
        }
      } catch (error) {
        console.error('Error fetching sensor data:', error);
      }
    }, 1000); // Poll every second

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, [navigate]);

  return (
    <>
      <Helmet>
        <title>HypTech</title>
        <meta name="description" content="Web site created using create-react-app" /> 
      </Helmet>
      <div className="flex h-screen w-full items-center justify-center bg-white-A700 bg-[url(/public/images/bg.png)] bg-cover bg-no-repeat">
        <div className="flex flex-col items-center justify-center h-full w-full p-5">
          <div className="relative flex flex-col items-center justify-center h-full w-full">
            <Img
              src="images/logo.png"
              alt="logoone"
              className="max-h-[50%] max-w-[50%] object-contain"
            />
            <Text
              size="2xl"
              as="p"
              className="mt-6 !text-with-shadow !font-bakbak-one tracking-[12.40px] !text-customgray text-center"
            >
              Boarding House Name
            </Text>
          </div>
        </div>
      </div>
    </>
  );
}

export default SplashscreenPage;
