"use client";

import Logo from "../components/logo";
import React from "react";
import { Tabs, Tab, Input, Link, Button, Card, CardBody } from "@nextui-org/react";

export default function Authentication() {
    const [selected, setSelected] = React.useState("login");

    return <div className="h-screen w-screen bg-neutral-100 flex flex-col items-center ">
        <div className="flex items-center h-20 px-6">
            <Logo />
        </div>
        <div style={{
            height: "calc(100% - 120px)",
        }}
            className="w-[75%] h-full rounded-xl flex items-center justify-center">
            <div className="flex flex-col items-center justify-center w-full h-full">
                <Card className="max-w-full w-[340px] h-[400px]">
                    <CardBody className="overflow-hidden">
                        <Tabs
                            fullWidth
                            aria-label="Tabs form"
                            selectedKey={selected}
                            size="md"
                            onSelectionChange={setSelected}
                        >
                            <Tab key="login" title="Login">
                                <form className="flex flex-col gap-4">
                                    <Input isRequired label="Email" placeholder="Enter your email" type="email" />
                                    <Input
                                        isRequired
                                        label="Password"
                                        placeholder="Enter your password"
                                        type="password"
                                    />
                                    <p className="text-center text-small">
                                        Need to create an account?{" "}
                                        <Link size="sm" onPress={() => setSelected("sign-up")}>
                                            Sign up
                                        </Link>
                                    </p>
                                    <div className="flex gap-2 justify-end">
                                        <Button fullWidth color="primary">
                                            Login
                                        </Button>
                                    </div>
                                </form>
                            </Tab>
                            <Tab key="sign-up" title="Sign up">
                                <form className="flex flex-col gap-4 h-[300px]">
                                    <Input isRequired label="Name" placeholder="Enter your name" type="password" />
                                    <Input isRequired label="Email" placeholder="Enter your email" type="email" />
                                    <Input
                                        isRequired
                                        label="Password"
                                        placeholder="Enter your password"
                                        type="password"
                                    />
                                    <p className="text-center text-small">
                                        Already have an account?{" "}
                                        <Link size="sm" onPress={() => setSelected("login")}>
                                            Login
                                        </Link>
                                    </p>
                                    <div className="flex gap-2 justify-end">
                                        <Button fullWidth color="primary">
                                            Sign up
                                        </Button>
                                    </div>
                                </form>
                            </Tab>
                        </Tabs>
                    </CardBody>
                </Card>
            </div>
        </div>
    </div>
};