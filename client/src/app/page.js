"use client";

import Logo from "./components/logo";
import React, { useState, useContext } from "react";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import AuthContext from "./context/AuthProvider";
import { Tabs, Tab, Input, Link, Button, Card, CardBody } from "@nextui-org/react";
import api from "./api/api"; // Ensure this import is correct

export default function Authentication() {
    const REGISTER_URL = '/users/';

    const [error, setError] = useState(null);

    const { register, handleSubmit, formState: { errors } } = useForm();

    const router = useRouter();

    const { loginApiCall } = useContext(AuthContext);

    const onSubmit = async (data) => {
        const body = {
            username: data['email-login'],
            password: data['parola-login'],
        };

        console.log(body);

        try {
            const response = await loginApiCall(body);
            if (response === 200) {
                setError(null);
                router.push('/homepage');
            }
        } catch (error) {
            if (!error.response) {
                setError('Server could not be contacted.');
            } else if (error.response.status === 401) {
                setError('Incorrect email or password.');
            } else {
                setError('Data could not be processed.');
            }
        }
    }

    const onSubmitRegister = async (data) => {
        try {

            const body = {
                email: data['email-register'],
                first_name: data['first_name'],
                last_name: data['last_name'],
                password: data['password-register'],
                role_id: 1,
            };

            console.log("BOOOOOOODY", body);

            await api.post(REGISTER_URL, body,
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    withCredentials: true,
                }
            );

            setSelected("login");
            setError(null);
        } catch (error) {
            if (!error.response) {
                setError('Server could not be contacted.');
            } else if (error.response.status === 409) {
                setError('Email already in use.');
            } else {
                setError('Data could not be processed.');
            }
        }
    }
    const [selected, setSelected] = React.useState("login");

    return (
        <div className="h-screen w-screen bg-neutral-100 flex flex-col items-center">
            <div className="flex items-center h-20 px-6">
                <Logo />
            </div>
            <div
                style={{ height: "calc(100% - 120px)" }}
                className="w-[75%] h-full rounded-xl flex items-center justify-center"
            >
                <div className="flex flex-col items-center justify-center w-full h-full">
                    <Card className="max-w-full w-[340px] h-auto">
                        <CardBody className="overflow-hidden">
                            <Tabs
                                fullWidth
                                aria-label="Tabs form"
                                selectedKey={selected}
                                size="md"
                                onSelectionChange={setSelected}
                            >
                                <Tab key="login" title="Login">
                                    <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
                                        <Input
                                            isRequired
                                            label="Email"
                                            placeholder="Enter your email"
                                            type="email"
                                            id="email-login"
                                            {...register("email-login")}
                                        />
                                        <Input
                                            isRequired
                                            label="Password"
                                            placeholder="Enter your password"
                                            type="password"
                                            id="parola-login"
                                            {...register("parola-login")}
                                        />
                                        <p className="text-center text-small">
                                            Need to create an account?{" "}
                                            <Link size="sm" onPress={() => setSelected("sign-up")}>
                                                Sign up
                                            </Link>
                                        </p>
                                        <div className="flex gap-2 justify-end">
                                            <Button fullWidth color="primary" type="submit">
                                                Login
                                            </Button>
                                        </div>
                                    </form>
                                    {error && <p className="text-red-500 text-sm text-center pt-4">{error}</p>}
                                </Tab>
                                <Tab key="sign-up" title="Sign up">
                                    <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmitRegister)}>
                                        <Input id="first_name" isRequired label="First Name" {...register("first_name")} placeholder="Enter your first name" type="text" />
                                        <Input id="last_name" isRequired label="Last Name" {...register("last_name")} placeholder="Enter your last name" type="text" />
                                        <Input id="email-register" isRequired label="Email" {...register("email-register")} placeholder="Enter your email" type="email" />
                                        <Input id="password-register" isRequired label="Password" {...register("password-register")} placeholder="Enter your password" type="password" />
                                        <p className="text-center text-small">
                                            Already have an account?{" "}
                                            <Link size="sm" onPress={() => setSelected("login")}>
                                                Login
                                            </Link>
                                        </p>
                                        <div className="flex gap-2 justify-end">
                                            <Button fullWidth color="primary" type="submit">
                                                Sign up
                                            </Button>
                                        </div>
                                    </form>
                                    {error && <p className="text-red-500 text-sm text-center pt-4">{error}</p>}
                                </Tab>
                            </Tabs>
                        </CardBody>
                    </Card>
                </div>
            </div>
        </div>
    );
}