from .models import Sample, SampleSerializer, Attribute, Job, Test

const SampleList = () => {

            let [samples, setSamples] = useState([])

            useEffect(() => {
                getSamples()
            }, [])

            let getSamples = async () => {

                let response = await fetch('/samples')
                let data = await response.json()
                setSamples(data)
            }

            return (
                <div className="samples">
                    <div className="samples-header">
                        <h2 className="samples-title">&#9782; Samples</h2>
                        <p className="samples-count">{samples.length}</p>
                    </div>

                    <div className="samples-list">
                        {samples.map((sample, index) => (
                            <div>
                                <div className="samples-list-item" >
                                    <h3>{sample.sample_id}</h3>
                                    <p>{sample.batch}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        }