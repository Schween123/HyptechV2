import { Helmet } from "react-helmet";
import { useNavigate } from 'react-router-dom';

const globalStyles = `
  body, html {
    background-color: #C5C3C6; 
    height: 100%;
    margin: 0;
  }
  #root, .app {
    height: 100%;
  }

  @media (max-width: 768px) {
    .responsive-container {
      flex-direction: column;
      padding: 20px;
    }

    .responsive-box {
      width: 100%;
      margin-bottom: 20px;
    }

    .responsive-text {
      font-size: 1.5rem;
    }

    .responsive-button {
      bottom: 20px;
      right: 20px;
      width: 40px;
      height: 40px;
    }
  }
`;

export default function BoarderFaceRegistrationPage() {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/billregistration'); // Adjust the path if needed
  };

  return ( 
    <>
      <Helmet>
        <title>HypTech</title>
        <meta name="description" content="Web site created using create-react-app" /> 
        <style>{globalStyles}</style>
      </Helmet>
      <div className="relative flex w-full h-full justify-between py-[100px] px-[100px] responsive-container">
        {/* Left side for image */}
        <div className="flex flex-col items-center justify-center w-[45%] bg-white p-5 rounded-lg shadow-lg responsive-box">
          <img 
            src="/path/to/image.jpg" 
            alt="User" 
            className="w-[150px] h-[150px] rounded-full mb-4"
          />
        </div>

        {/* Right side for info */}
        <div className="flex flex-col justify-center w-[45%] bg-white p-5 rounded-lg shadow-lg responsive-box">
          <h2 className="text-2xl font-semibold mb-4 responsive-text">User Information</h2>
          <div className="flex flex-col space-y-2 responsive-text">
            <p><strong>Name:</strong> John Doe</p>
            <p><strong>Gender:</strong> Male</p>
            <p><strong>Age:</strong> 25</p>
            <p><strong>Address:</strong> 123 Main Street, Cityville</p>
            <p><strong>Contact number:</strong> 09123456789</p>
            <p><strong>Course/Profession:</strong> Software Engineer</p>
            <p><strong>School/Company:</strong> Tech University / Tech Corp</p>
            <p><strong>Guardian's name:</strong> Jane Doe</p>
            <p><strong>Guardian's Address:</strong> 456 Another Street, Cityville</p>
            <p><strong>Guardian's contact number:</strong> 09876543210</p>
            <p><strong>Relationship with guardian:</strong> Mother</p>
          </div>
        </div>

        {/* Next button positioned at the lower right corner */}
        <button 
          onClick={handleButtonClick} 
          className="absolute bottom-10 right-10 bg-transparent border-none cursor-pointer responsive-button">
          <img src="public/images/nxtbtn2.png" alt="Next" className="w-[50px] h-[50px]" />
        </button>
      </div>
    </>
  );
}
