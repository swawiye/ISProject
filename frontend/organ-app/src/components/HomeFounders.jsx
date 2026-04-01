import HomeNav from "./HomeNav";

function Founders() {
    return (
        <>
            <HomeNav />
            {/* Hero section */}
            <header>
                <div className='relative w-full overflow-hidden'>
                    <img src="src\assets\hero.jpg" alt="hero" className='w-full h-auto object-cover block' style={{ minHeight: "40vh", maxHeight: "80vh" }} />
                </div>
            </header>
        </>
    );
}
export default Founders;