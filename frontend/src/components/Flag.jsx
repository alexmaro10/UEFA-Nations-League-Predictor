import { CODE_TO_ISO } from '../utils/flags'

function Flag({ code, className = '' }) {
	const iso = CODE_TO_ISO[code]

	if (!iso) return null

	return <span style={{ borderRadius: '100%', height: '25px', width: '25px' }} className={`fi fi-${iso} ${className} `} />
}

export default Flag