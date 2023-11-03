import React from 'react';
import styled from 'styled-components';

const LoginpageContainer = styled.div`
  position: relative;
  z-index: 0;
  height: 100vh;
  width: 100%;
  background-color: #f4f3f3;
  border: 1px solid #000000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const Rectangle1 = styled.div`
  position: absolute;
  top: 350px;
  left: 50;
  z-index: 1;
  border-radius: 40px;
  height: 600px;
  width: 1230px;
  background-color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.1); 
`;

const PWinput = styled.div`
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  margin-bottom: 10 px;
`;

const LabelContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0px 0px 8px 0px;
  gap: 10px;
`;

//비밀번호
const PWtext = styled.div`
  text-align: left;
  vertical-align: top;
  font-size: 20px;
  font-family: 'IBM Plex Sans';
  letter-spacing: -1 px;
  line-height: 40px;
  color: #525252;
  font-weight: bold;
`;

const Field = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  background-color: #ffffff;
  border: 2px solid #ed174d;
`;

const TextIcon = styled.div`
  height: 60px;
  width: 564px;
`;

const InputText = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
`;
// 비밀번호를 입력해주세요
const PWinputtext = styled.div` 
  text-align: left;
  vertical-align: top;
  font-size: 16px;
  font-family: 'IBM Plex Sans';
  letter-spacing: 0.16px;
  line-height: 60px;
  color: #a8a8a8;
`;

const HelperTextContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 4px 0px 0px 0px;
  gap: 10px;
`;

const Text3 = styled.div`
  text-align: left;
  vertical-align: top;
  font-size: 15px;
  font-family: 'IBM Plex Sans';
  letter-spacing: 0.32px;
  line-height: 16px;
  color: #525252;
`;

const IDinput = styled.div`
  z-index: 3;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  margin-top: 200px;
  margin-bottom: 10px;

`;
// 아이디/이메일 주소
const IDtext = styled.div`
  text-align: left;
  vertical-align: top;
  font-size: 20px;
  font-family: 'IBM Plex Sans';
  letter-spacing: -1 px;
  line-height: 40px;
  color: #525252;
  font-weight: bold; 
`;

const Field2 = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  background-color: #ffffff;
  border: 2px solid #ed174d;
`;

const TextIcon2 = styled.div`
  height: 60px;
  width: 564px;
`;

const InputText2 = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
`;

// 아이디를 입력해주세요
const IDinputtext = styled.div`
  text-align: left;
  vertical-align: top;
  font-size: 16px;
  font-family: 'IBM Plex Sans';
  letter-spacing: -0.2px;
  line-height: 60px;
  color: #a8a8a8;
`;

const Header = styled.div`
  z-index: 2;
  height: 90px;
  width: 100%;
  background-color: #ed174d;
  position: absolute;
  top: 50px;
`;

const ButtonLogin = styled.button`
  z-index: 2;
  border: none; /* Removed border */
  border-radius: 25px;
  width: 175px; /* Set width */
  height: 50px; /* Set height */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 10px;
  gap: 10px;
  background-color: #cfcfcf;
  cursor: pointer;
  font-weight: bold;
  margin-top: 40px;
`;

const ButtonText = styled.div`
  text-align: center;
  vertical-align: middle;
  font-size: 18px;
  font-family: 'Inter';
  letter-spacing: -0.5%;
  line-height: 100%;
  color: #000000;
`;

const Img = styled.img`
  position: absolute;
  top: 230px; /* Adjusted top position */
  left: 50;
  z-index: 3;
  height: 175.5px;
  width: 299px;
`;

const Text = styled.div`
  z-index: 3;
  display: flex;
  flex-direction : row;
  margin-top : 10px;
`;

const Text8 = styled.div`
  text-align: left;
  vertical-align: top;
  font-size: 18px;
  font-family: 'Mako';
  letter-spacing: -0.5px;
  line-height: 25px;
  color: #000000;
  flex-direction: column;
  margin-right: 30px;
`;

const TextFindPW = styled.div`
  text-align: right;
  vertical-align: top;
  font-size: 18px;
  font-family: 'Mako';
  letter-spacing: -0.5px;
  line-height: 25px;
  color: #000000;
  flex-direction: column;
`;

const Loginpage = () => {
  return (
    <LoginpageContainer>
      <Header />
      <Rectangle1 />
      <Img src="/hello.png" alt="hello" />
      <IDinput>
        <IDtext>아이디 / 이메일주소</IDtext>
        <Field2>
          <TextIcon2>
            <InputText2 />
            <IDinputtext> 아이디를 입력해주세요.</IDinputtext>
          </TextIcon2>
        </Field2>
      </IDinput>
      <PWinput>
        <LabelContainer>
          <PWtext>비밀번호</PWtext>
        </LabelContainer>
        <Field>
          <TextIcon>
            <InputText />
            <PWinputtext> 비밀번호를 입력해주세요.</PWinputtext>
          </TextIcon>
        </Field>
        <HelperTextContainer>
          <Text3>최소 10자리 이상 입력</Text3>
        </HelperTextContainer>
      </PWinput>
      <ButtonLogin>
        <ButtonText>로그인</ButtonText>
      </ButtonLogin>
      <Text>
        <Text8>회원이 아니라면?</Text8>
        <TextFindPW>비밀번호 찾기</TextFindPW>
      </Text>
    </LoginpageContainer>
  );
};

export default Loginpage;
